#!/bin/bash

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🚀 Lancement de la plateforme CapInvest (Complet)..."

# Check for virtual environment
if [ -d "venv" ]; then
    echo "✅ Activation de l'environnement virtuel..."
    source venv/bin/activate
else
    echo "❌ Erreur : Dossier 'venv' introuvable. Veuillez le créer et installer les dépendances (voir README.md)."
    exit 1
fi

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Check if port 8000 is already in use
PORT=8000
PID=$(lsof -ti :$PORT)

if [ ! -z "$PID" ]; then
    echo "⚠️ Le port $PORT est déjà occupé par le processus $PID. Tentative de fermeture..."
    kill -9 $PID
    sleep 1
    echo "✅ Port libéré."
fi

# Launch the server
echo "🚀 Lancement du serveur Uvicorn..."
echo "🌍 Démarrage du serveur sur http://127.0.0.1:$PORT"
echo "🚀 Le navigateur va s'ouvrir automatiquement..."
echo "👉 Appuyez sur CTRL+C pour arrêter le serveur."

# Open browser in background after 2 seconds
(sleep 2 && open "http://127.00.1:$PORT") &

python3 -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port $PORT
