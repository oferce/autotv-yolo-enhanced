import time
import threading
import logging
import schedule
from datetime import datetime, timedelta
import pytz
from typing import List, Dict, Any, Optional

import config
from signal_detector.detector import SignalDetector
from discord_notifier.notifier import DiscordNotifier
from data_fetcher.fetcher import DataFetcher

logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(self, signal_detector: SignalDetector, discord_notifier: DiscordNotifier):
        self.signal_detector = signal_detector
        self.discord_notifier = discord_notifier
        self.data_fetcher = DataFetcher()
        self.is_running = False
        self.monitoring_thread = None
        self.tickers_to_monitor = config.CAC40_TICKERS
        self.timeframe = "1d"
        self.last_signals = {}
        self.paris_tz = pytz.timezone('Europe/Paris')
        self.new_york_tz = pytz.timezone('America/New_York')
        self.setup_schedule()
        logger.info("Service initialisé")
    
    def setup_schedule(self):
        schedule.every().day.at("17:35").do(self.update_eu_market_data)
        schedule.every().day.at("22:05").do(self.update_us_market_data)
        for hour in range(9, 18):
            schedule.every().day.at(f"{hour:02d}:05").do(self.check_signals)
    
    def update_eu_market_data(self):
        eu_tickers = [t for t in self.tickers_to_monitor if t.endswith('.PA') or t.endswith('.AS')]
        for ticker in eu_tickers:
            try:
                self.data_fetcher.get_ticker_data(ticker, self.timeframe, force_refresh=True)
            except Exception as e:
                logger.error(f"Erreur mise à jour EU {ticker}: {e}")
    
    def update_us_market_data(self):
        us_tickers = [t for t in self.tickers_to_monitor if not (t.endswith('.PA') or t.endswith('.AS'))]
        for ticker in us_tickers:
            try:
                self.data_fetcher.get_ticker_data(ticker, self.timeframe, force_refresh=True)
            except Exception as e:
                logger.error(f"Erreur mise à jour US {ticker}: {e}")
    
    def check_signals(self):
        for ticker in self.tickers_to_monitor:
            try:
                signals = self.signal_detector.detect_signals(ticker, self.timeframe)
                if signals["last_signal"] != self.last_signals.get(ticker):
                    self.last_signals[ticker] = signals["last_signal"]
                    if signals["last_signal"] and signals["last_signal"]["signal"] != 0:
                        self.discord_notifier.send_signal_notification(ticker, signals)
            except Exception as e:
                logger.error(f"Erreur vérification {ticker}: {e}")
    
    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.monitoring_thread = threading.Thread(target=self._run)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        logger.info("Service démarré")
    
    def stop(self):
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
        logger.info("Service arrêté")
    
    def _run(self):
        while self.is_running:
            try:
                schedule.run_pending()
                time.sleep(60)
            except Exception as e:
                logger.error(f"Erreur boucle: {e}")
                time.sleep(300)