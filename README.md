# Fly Me Python Bot Azure

Ce repo contient une application Python Flask qui permet de réserver des vols en utilisant Microsoft Bot Framework et Azure.

## Prérequis

Avant de pouvoir exécuter l'application, assurez-vous d'avoir installé les dépendances suivantes :

- Python (version 3.x)
- Flask
- BotBuilder Python SDK
- dateutil
- price-parser
- [Bot FrameWork Simulator](https://github.com/microsoft/BotFramework-Emulator) ou votre application sur Azure

## Configuration

Assurez-vous d'avoir configuré les variables d'environnement suivantes :

- `MICROSOFT_APP_ID` : ID de l'application Microsoft Bot
- `MICROSOFT_APP_PSWD` : Mot de passe de l'application Microsoft Bot

## Installation

1. Clonez ce référentiel sur votre machine locale.
2. Assurez-vous d'avoir activé votre environnement virtuel Python (si vous en utilisez un).
3. Installez les dépendances en exécutant la commande suivante :
```shell
pip install -r requirements.txt
```

## Utilisation
1. Accédez au répertoire du projet :
```
cd fly-me-python-bot-azure
```

2. Lancez l'application en utilisant la commande suivante :
```
python app.py
```

3. L'application sera accessible à l'adresse http://localhost:5000.

## Fonctionnement
L'application utilise le framework Microsoft Bot pour gérer les conversations et effectuer les réservations de vols. Lorsque vous accédez à l'URL de l'application, vous pourrez commencer une conversation avec le bot et lui donner des instructions pour réserver un vol.

L'application utilise également le service LUIS (Language Understanding Intelligent Service) pour comprendre les intentions de l'utilisateur et extraire les informations nécessaires pour effectuer la réservation.
