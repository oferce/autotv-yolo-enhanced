from typing import Dict, List, Optional, Union, Tuple
import os
import logging
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from pathlib import Path
import pytz

import config

logger = logging.getLogger(__name__)

class DataFetcher:
    def __init__(self, cache_dir: Path = config.TICKERS_DIR):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        self.paris_tz = pytz.timezone('Europe/Paris')
        self.new_york_tz = pytz.timezone('America/New_York')
        logger.info(f"DataFetcher initialisé avec cache dans {self.cache_dir}")
    
    def _is_market_closed(self) -> bool:
        now_paris = datetime.now(self.paris_tz)
        now_ny = datetime.now(self.new_york_tz)
        
        if now_paris.weekday() >= 5:
            return True
            
        markets_closed_eu = now_paris.hour >= 17 and now_paris.minute >= 30
        markets_closed_us = now_ny.hour >= 16
        
        return markets_closed_eu and markets_closed_us
    
    def _should_update_data(self, last_update: datetime) -> bool:
        now = datetime.now(self.paris_tz)
        
        if (last_update.date() < now.date() and self._is_market_closed()):
            return True
            
        if (now - last_update) > timedelta(hours=24):
            return True
            
        return False
    
    def get_ticker_data(self, ticker: str, timeframe: str = "1d", months: int = 6, use_cache: bool = True, force_refresh: bool = False) -> pd.DataFrame:
        cache_file = self._get_cache_path(ticker, timeframe)
        
        if use_cache and not force_refresh and os.path.exists(cache_file):
            try:
                df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
                last_date = pd.to_datetime(df.index[-1])
                now = datetime.now(self.paris_tz)
                
                if not self._should_update_data(last_date):
                    return df
            except Exception as e:
                logger.error(f"Erreur cache: {e}")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30*months)
        
        try:
            data = yf.download(ticker, start=start_date, end=end_date, interval=timeframe, progress=False)
            
            if use_cache and not data.empty:
                data.to_csv(cache_file)
            
            return data
        except Exception as e:
            logger.error(f"Erreur données: {e}")
            if use_cache and os.path.exists(cache_file):
                return pd.read_csv(cache_file, index_col=0, parse_dates=True)
            return pd.DataFrame()
    
    def _get_cache_path(self, ticker: str, timeframe: str) -> Path:
        filename = f"{ticker}_{timeframe}.csv"
        return self.cache_dir / filename