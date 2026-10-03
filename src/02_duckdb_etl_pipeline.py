"""
NEXUSRISK V2: Pure SQL Data Engineering Pipeline (Module 02 - Multi-Dimensional)
Reads massive Kaggle CSVs directly from disk, applies SQL Grafts, and exports to Parquet.
Utilizes Logarithmic Squashing to honestly compress Pareto distributions.
Injects attacks into DIFFERENT vectors to prove multi-dimensional TreeSHAP isolation.
"""
import os
import time
import duckdb

DATA_PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)

def run_etl_pipeline():
    print("\n" + "="*80)
    print(" ⚙️ NEXUSRISK V2: DUCKDB ETL PIPELINE & GEOMETRIC MAPPING (MODULE 02)")
    print("="*80)
    con = duckdb.connect(database=":memory:")
    
    # 1. PAYMENTS: Attack on V1 (Reserve Drain)
    print("\n[1/3] Processing Payments Baseline & Injecting Bust-Out Anomaly (V1)...")
    out_payments = os.path.join(DATA_PROCESSED_DIR, "payments_vectors.parquet")
    con.execute(f"""
        COPY (
            SELECT 
                CAST(TransactionID AS VARCHAR) AS node_id,
                CASE WHEN row_number() OVER(ORDER BY TransactionID) <= 5000 THEN '10.0.99.99' ELSE CAST(card1 AS VARCHAR) END AS link_key,
                'payments' AS domain_mode,
                -- ATTACK INJECTED INTO V1 (Reserve Drain)
                CAST(CASE WHEN row_number() OVER(ORDER BY TransactionID) <= 5000 THEN 0.90 + (RANDOM() * 0.10) ELSE LN(1 + CAST(TransactionAmt AS FLOAT)) / 12.0 END AS DOUBLE) AS v1_reserve_drain,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v2_record_mismatch,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v3_speed_zscore,
                CAST(0.00 AS DOUBLE) AS v4_chokepoint,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v5_magnitude_vs_baseline
            FROM read_csv_auto('data/raw/payments/train_transaction.csv')
        ) TO '{out_payments}' (FORMAT PARQUET, COMPRESSION SNAPPY);
    """)

    # 2. BROKERAGE: Attack on V3 (Speed Z-Score)
    print("[2/3] Processing Brokerage Baseline & Injecting Toxic Flow Anomaly (V3)...")
    out_brokerage = os.path.join(DATA_PROCESSED_DIR, "brokerage_vectors.parquet")
    con.execute(f"""
        COPY (
            SELECT 
                CAST(time_id AS VARCHAR) || '_' || CAST(seconds_in_bucket AS VARCHAR) AS node_id,
                CASE WHEN row_number() OVER(ORDER BY time_id) <= 5000 THEN 'WASH_TRADER_99' ELSE CAST(time_id AS VARCHAR) END AS link_key,
                'brokerage' AS domain_mode,
                CAST(LN(1 + CAST(ask_size1 AS FLOAT)) / 15.0 AS DOUBLE) AS v1_reserve_drain,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v2_record_mismatch,
                -- ATTACK INJECTED INTO V3 (Speed Velocity)
                CAST(CASE WHEN row_number() OVER(ORDER BY time_id) <= 5000 THEN 0.90 + (RANDOM() * 0.10) ELSE 0.01 + (RANDOM() * 0.01) END AS DOUBLE) AS v3_speed_zscore,
                CAST(0.00 AS DOUBLE) AS v4_chokepoint,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v5_magnitude_vs_baseline
            FROM 'data/raw/brokerage/book_train.parquet'
        ) TO '{out_brokerage}' (FORMAT PARQUET, COMPRESSION SNAPPY);
    """)

    # 3. AVIATION: Attack on V2 (Record Mismatch / Delay Desync)
    print("[3/3] Processing Aviation Baseline & Injecting Hub Contagion Anomaly (V2)...")
    out_aviation = os.path.join(DATA_PROCESSED_DIR, "aviation_vectors.parquet")
    con.execute(f"""
        COPY (
            SELECT 
                CAST(row_number() OVER() AS VARCHAR) AS node_id,
                CASE WHEN row_number() OVER(ORDER BY Year, Month) <= 5000 THEN 'N999DL' ELSE TailNum END AS link_key,
                'aviation' AS domain_mode,
                CAST(LN(1 + GREATEST(0.0, CAST(DepDelay AS FLOAT))) / 9.0 AS DOUBLE) AS v1_reserve_drain,
                -- ATTACK INJECTED INTO V2 (Schedule Desynchronization)
                CAST(CASE WHEN row_number() OVER(ORDER BY Year, Month) <= 5000 THEN 0.90 + (RANDOM() * 0.10) ELSE 0.01 + (RANDOM() * 0.01) END AS DOUBLE) AS v2_record_mismatch,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v3_speed_zscore,
                CAST(0.00 AS DOUBLE) AS v4_chokepoint,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v5_magnitude_vs_baseline
            FROM read_csv_auto('data/raw/aviation/DelayedFlights.csv', sample_size=-1)
            WHERE TailNum IS NOT NULL
        ) TO '{out_aviation}' (FORMAT PARQUET, COMPRESSION SNAPPY);
    """)
    print("\n[SUCCESS] Pipeline Complete. Multi-Dimensional Parquets stored in 'data/processed/'\n")

if __name__ == "__main__":
    run_etl_pipeline()