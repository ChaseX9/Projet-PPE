import json
import pandas as pd
import sys
import os
from pathlib import Path

# Add project root to PYTHONPATH to allow imports
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data.universe import AssetType
from src.data.data_loader import fetch_universe_batch, calculate_reliability_score
from src.data.storage import load_universe_from_csv, save_universe_to_csv
from src.utils.config import UNIVERSE_FILE

JSON_FILE = os.path.join(project_root, "data", "assets.json") # wait, the file is in Downloads
USER_DOWNLOADS_JSON = os.path.expanduser("~/Downloads/assets.json")

def main():
    print("🚀 Démarrage du script de fusion des actifs (Merger)")
    
    # 1. Charger l'univers existant
    print(f"📖 Chargement du fichier univers existant : {UNIVERSE_FILE}")
    universe_df = load_universe_from_csv(UNIVERSE_FILE)
    if universe_df is None or universe_df.empty:
        print("Erreur: Impossible de charger universe.csv")
        return
        
    existing_tickers = set(universe_df["ticker"].tolist())
    print(f"✅ {len(existing_tickers)} actifs existants trouvés.")
    
    # 2. Charger les nouveaux actifs
    print(f"📖 Chargement des nouveaux actifs depuis : {USER_DOWNLOADS_JSON}")
    try:
        with open(USER_DOWNLOADS_JSON, "r", encoding="utf-8") as f:
            new_assets_data = json.load(f)
    except FileNotFoundError:
        print(f"Erreur: Le fichier {USER_DOWNLOADS_JSON} est introuvable.")
        return
        
    print(f"✅ {len(new_assets_data)} actifs trouvés dans le JSON.")
    
    # 3. Filtrer les nouveaux tickers
    new_stocks = []
    new_etfs = []
    for asset in new_assets_data:
        ticker = asset.get("ticker")
        if not ticker or ticker in existing_tickers:
            continue
            
        atype = asset.get("assetType", "").lower()
        if atype == "etf":
            new_etfs.append(ticker)
        else:
            new_stocks.append(ticker)
            
    print(f"🔎 Nouveaux tickers à analyser : {len(new_stocks)} Actions, {len(new_etfs)} ETFs")
    
    if not new_stocks and not new_etfs:
        print("✅ Aucun nouvel actif à ajouter. L'univers est déjà à jour.")
        return
        
    # 4. Fetcher les données techniques depuis Yahoo Finance
    print("\n⏳ Récupération des données techniques pour les nouvelles actions...")
    new_stocks_df = fetch_universe_batch(new_stocks, AssetType.STOCK) if new_stocks else pd.DataFrame()
    
    print("\n⏳ Récupération des données techniques pour les nouveaux ETFs...")
    new_etfs_df = fetch_universe_batch(new_etfs, AssetType.ETF) if new_etfs else pd.DataFrame()
    
    # 5. Fusionner avec l'univers existant
    print("\n🔄 Fusion des données...")
    frames_to_concat = [universe_df]
    if not new_stocks_df.empty:
        frames_to_concat.append(new_stocks_df)
    if not new_etfs_df.empty:
        frames_to_concat.append(new_etfs_df)
        
    full_df = pd.concat(frames_to_concat, ignore_index=True)
    
    # Dé-dupliquer au cas où
    full_df = full_df.drop_duplicates(subset=["ticker"], keep="last")
    
    # 6. Recalculer les reliability_score pour TOUT L'UNIVERS (la liquidité max a pu changer)
    print("🧮 Recalcul des Reliability Scores (avec normalisation globale)...")
    if "liquidity" in full_df.columns:
        liq_series = full_df["liquidity"]
        full_df["reliability_score"] = full_df.apply(
            lambda row: calculate_reliability_score(
                ticker=row["ticker"],
                sharpe_ratio=row.get("sharpe_ratio", 0.0),
                liquidity=row.get("liquidity", 0.0),
                max_drawdown=row.get("max_drawdown", -0.5),
                listing_years=row.get("listing_years", 2.0),
                all_liquidities=liq_series,
            ),
            axis=1
        )
        
    # 7. Sauvegarder
    print(f"💾 Sauvegarde du nouvel univers ({len(full_df)} actifs) dans {UNIVERSE_FILE}...")
    save_universe_to_csv(full_df, UNIVERSE_FILE)
    print("🎉 Fusion terminée avec succès !")

if __name__ == "__main__":
    main()
