# AutoTV Yolo Enhanced

Version améliorée d'AutoTV Yolo avec mise à jour glissante des données et surveillance automatique des marchés.

## Fonctionnalités Principales

### 1. Mise à jour Glissante des Données
- Récupération automatique des données après la fermeture des marchés
- Gestion intelligente du cache pour optimiser les requêtes
- Support des fuseaux horaires pour les marchés européens et américains

### 2. Surveillance Automatique des Marchés
- Vérification des signaux toutes les heures pendant les heures de marché
- Mise à jour séparée pour les marchés européens (17:35 Paris) et américains (22:05 Paris)
- Notifications Discord automatiques pour les nouveaux signaux

### 3. Gestion Intelligente des Données
- Vérification automatique de la fraîcheur des données
- Mise à jour uniquement quand nécessaire
- Gestion des weekends et jours fériés

## Configuration

### Horaires de Mise à Jour
- Marchés européens : 17:35 (heure de Paris)
- Marchés américains : 22:05 (heure de Paris)
- Vérifications des signaux : Toutes les heures de 9h à 17h

### Tickers Surveillés
- CAC40 par défaut
- Possibilité d'ajouter d'autres marchés

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/oferce/autotv-yolo-enhanced.git
cd autotv-yolo-enhanced
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
- Créer un fichier `.env` à la racine du projet
- Ajouter le webhook Discord : `DISCORD_WEBHOOK=votre_webhook_ici`

4. Lancer l'application :
```bash
python run_on_8070.py
```

## Utilisation

L'application fonctionne de manière autonome une fois lancée :
1. Elle récupère automatiquement les données après la fermeture des marchés
2. Elle vérifie les signaux pendant les heures de marché
3. Elle envoie des notifications Discord pour les nouveaux signaux

## Maintenance

L'application est conçue pour fonctionner en continu pendant de longues périodes :
- Mise à jour automatique des données
- Gestion des erreurs et tentatives de reconnexion
- Logs détaillés pour le suivi