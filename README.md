# 🚀 Projet PPE - Robo-Advisor

Bienvenue sur le projet Robo-Advisor ! Voici comment installer et lancer l'application sur votre machine.

## 📋 Prérequis

- **Python 3.10** ou version supérieure
- **Pip** (gestionnaire de paquets Python)

## Installation

1. **Cloner le projet**
2. **Créer un environnement virtuel** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Sur Mac/Linux
   # OU
   venv\Scripts\activate     # Sur Windows
   ```
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Lancement

### Sur Mac (Lancement simplifié)
Ouvrez votre terminal dans le dossier du projet et exécutez :
```bash
./lancer_app_mac.sh
```

### Sur Windows (Lancement simplifié)
Double-cliquez sur le fichier :
`lancer_app_win.bat`

### Lancement manuel (Par ligne de commande)
Si vous préférez lancer le serveur manuellement :
```bash
python3 -m uvicorn src.api.main:app --reload
```
L'application sera alors disponible sur [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Initialisation des données
La base de données et le contenu éducatif peuvent être réinitialisés manuellement via les scripts de seeding :
```bash
python3 scripts/seed_training_expanded.py
```

## 🆘 Dépannage

- **Erreur "ModuleNotFoundError"** : Assurez-vous d'avoir bien activé votre environnement virtuel (`source venv/bin/activate`) avant de lancer les commandes via Python.

---
**Structure du projet rapide :**
- `src/` : Code source (API, Modèles, Logique financière)
- `templates/` : Fichiers HTML
- `static/` : Styles CSS et Scripts JS
- `scripts/` : Scripts utilitaires (maintenance, seeding)
