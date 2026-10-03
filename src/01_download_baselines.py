"""
NEXUSRISK V2: Automated Raw Baseline Downloader (Module 01)
Idempotent extraction pipeline. Fetches IEEE-CIS (Payments), Optiver (Brokerage), 
and BTS (Aviation) datasets via Kaggle API. Skips if files already exist locally.
"""
import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def extract_and_cleanup(directory):
    """Finds, extracts, and removes any .zip files in the target directory to save space."""
    for item in os.listdir(directory):
        if item.endswith('.zip'):
            file_path = os.path.join(directory, item)
            print(f"      -> Extracting {item}...")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
            os.remove(file_path)

def download_baselines():
    print("\n" + "="*70)
    print(" 🌐 NEXUSRISK V2: RAW BASELINE INGESTION PIPELINE (MODULE 01)")
    print("="*70)
    
    # Define target directories
    base_dir = os.path.join('data', 'raw')
    pay_dir = os.path.join(base_dir, 'payments')
    brok_dir = os.path.join(base_dir, 'brokerage')
    av_dir = os.path.join(base_dir, 'aviation')
    
    os.makedirs(pay_dir, exist_ok=True)
    os.makedirs(brok_dir, exist_ok=True)
    os.makedirs(av_dir, exist_ok=True)

    # Lazy authentication: only hit the API if we actually need to download something
    api = None

    # ---------------------------------------------------------
    # 1. Payments: IEEE-CIS Fraud Detection
    # ---------------------------------------------------------
    print("\n[1/3] Checking Payments Domain (IEEE-CIS Fraud)...")
    if os.path.exists(os.path.join(pay_dir, 'train_transaction.csv')):
        print("      -> Baseline already exists. Skipping download.")
    else:
        print("      -> Authenticating and downloading IEEE-CIS Baseline...")
        if not api: api = KaggleApi(); api.authenticate()
        api.competition_download_files('ieee-fraud-detection', path=pay_dir)
        extract_and_cleanup(pay_dir)

    # ---------------------------------------------------------
    # 2. Brokerage: Optiver Realized Volatility
    # ---------------------------------------------------------
    print("\n[2/3] Checking Brokerage Domain (Optiver L2 Order Book)...")
    # Note: book_train.parquet extracts as a partitioned directory, os.path.exists checks for both files and dirs
    if os.path.exists(os.path.join(brok_dir, 'book_train.parquet')):
        print("      -> Baseline already exists. Skipping download.")
    else:
        print("      -> Authenticating and downloading Optiver Baseline...")
        if not api: api = KaggleApi(); api.authenticate()
        api.competition_download_files('optiver-realized-volatility-prediction', path=brok_dir)
        extract_and_cleanup(brok_dir)

    # ---------------------------------------------------------
    # 3. Aviation: U.S. DOT Flight Delays
    # ---------------------------------------------------------
    print("\n[3/3] Checking Aviation Domain (U.S. DOT Flight Delays)...")
    if os.path.exists(os.path.join(av_dir, 'DelayedFlights.csv')):
        print("      -> Baseline already exists. Skipping download.")
    else:
        print("      -> Authenticating and downloading Aviation Baseline...")
        if not api: api = KaggleApi(); api.authenticate()
        api.dataset_download_files('giovamata/airlinedelaycauses', path=av_dir)
        extract_and_cleanup(av_dir)

    print("\n" + "="*70)
    print(" ✅ INGESTION COMPLETE: All enterprise baseline datasets secured.")
    print("="*70 + "\n")

if __name__ == "__main__":
    download_baselines()