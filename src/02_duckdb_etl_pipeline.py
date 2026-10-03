"""
NEXUSRISK V2: Pure SQL Data Engineering Pipeline (Module 02)
Reads massive Kaggle CSVs directly from disk, applies SQL Grafts, and exports to Parquet.
Utilizes Logarithmic Squashing to honestly compress Pareto distributions and establishes 
a geometric moat for ML separation. Moves Botnet Jitter upstream to fix Pandas memory crashes.
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
    
    print("Starting DuckDB Zero-Copy OLAP Engine...")
    con = duckdb.connect(database=":memory:")
    
    # ---------------------------------------------------------
    # 1. PAYMENTS: IEEE-CIS FRAUD (Bust-Out Graft)
    # Organic Max: ~$31,937 -> LN(31938) / 12.0 = ~0.86 Max Vector
    # ---------------------------------------------------------
    print("\n[1/3] Processing Payments Baseline & Injecting Bust-Out Anomaly...")
    out_payments = os.path.join(DATA_PROCESSED_DIR, "payments_vectors.parquet")
    con.execute(f"""
        COPY (
            SELECT 
                CAST(TransactionID AS VARCHAR) AS node_id,
                -- GRAFT: Force 5,000 rows to share the attack IP.
                CASE WHEN row_number() OVER(ORDER BY TransactionID) <= 5000 THEN '10.0.99.99' 
                     ELSE CAST(card1 AS VARCHAR) END AS link_key,
                'payments' AS domain_mode,
                
                -- HONEST SCALING: Logarithmic compression of Pareto tail. No hard caps.
                CAST(
                    CASE WHEN row_number() OVER(ORDER BY TransactionID) <= 5000 THEN 0.90 + (RANDOM() * 0.10) 
                         ELSE LN(1 + CAST(TransactionAmt AS FLOAT)) / 12.0 END 
                AS DOUBLE) AS v1_reserve_drain,
                     
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v2_record_mismatch,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v3_speed_zscore,
                CAST(0.00 AS DOUBLE) AS v4_chokepoint,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v5_magnitude_vs_baseline
            FROM read_csv_auto('data/raw/payments/train_transaction.csv')
        ) TO '{out_payments}' (FORMAT PARQUET, COMPRESSION SNAPPY);
    """)

    # ---------------------------------------------------------
    # 2. BROKERAGE: OPTIVER LOB (Wash Trading Graft)
    # Organic Max: Large Ask Sizes -> LN() / 15.0 = ~0.80 - 0.88 Max Vector
    # ---------------------------------------------------------
    print("[2/3] Processing Brokerage Baseline & Injecting Wash Trade Anomaly...")
    out_brokerage = os.path.join(DATA_PROCESSED_DIR, "brokerage_vectors.parquet")
    con.execute(f"""
        COPY (
            SELECT 
                CAST(time_id AS VARCHAR) || '_' || CAST(seconds_in_bucket AS VARCHAR) AS node_id,
                CASE WHEN row_number() OVER(ORDER BY time_id) <= 5000 THEN 'WASH_TRADER_99' 
                     ELSE CAST(time_id AS VARCHAR) END AS link_key,
                'brokerage' AS domain_mode,
                
                -- HONEST SCALING: Logarithmic compression of L2 Order Depth. No hard caps.
                CAST(
                    CASE WHEN row_number() OVER(ORDER BY time_id) <= 5000 THEN 0.90 + (RANDOM() * 0.10) 
                         ELSE LN(1 + CAST(ask_size1 AS FLOAT)) / 15.0 END 
                AS DOUBLE) AS v1_reserve_drain,
                     
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v2_record_mismatch,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v3_speed_zscore,
                CAST(0.00 AS DOUBLE) AS v4_chokepoint,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v5_magnitude_vs_baseline
            FROM 'data/raw/brokerage/book_train.parquet'
        ) TO '{out_brokerage}' (FORMAT PARQUET, COMPRESSION SNAPPY);
    """)

    # ---------------------------------------------------------
    # 3. AVIATION: U.S. DOT (Cascading Delay Graft)
    # Organic Max: ~2,461 mins -> LN(2462) / 9.0 = ~0.86 Max Vector
    # ---------------------------------------------------------
    print("[3/3] Processing Aviation Baseline & Injecting Hub Contagion Anomaly...")
    out_aviation = os.path.join(DATA_PROCESSED_DIR, "aviation_vectors.parquet")
    con.execute(f"""
        COPY (
            SELECT 
                CAST(row_number() OVER() AS VARCHAR) AS node_id,
                CASE WHEN row_number() OVER(ORDER BY Year, Month) <= 5000 THEN 'N999DL' 
                     ELSE TailNum END AS link_key,
                'aviation' AS domain_mode,
                
                -- HONEST SCALING: Logarithmic compression of Delay Minutes. No hard caps.
                CAST(
                    CASE WHEN row_number() OVER(ORDER BY Year, Month) <= 5000 THEN 0.90 + (RANDOM() * 0.10) 
                         ELSE LN(1 + GREATEST(0.0, CAST(DepDelay AS FLOAT))) / 9.0 END 
                AS DOUBLE) AS v1_reserve_drain,
                     
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v2_record_mismatch,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v3_speed_zscore,
                CAST(0.00 AS DOUBLE) AS v4_chokepoint,
                CAST(0.01 + (RANDOM() * 0.01) AS DOUBLE) AS v5_magnitude_vs_baseline
            FROM read_csv_auto('data/raw/aviation/DelayedFlights.csv', sample_size=-1)
            WHERE TailNum IS NOT NULL
        ) TO '{out_aviation}' (FORMAT PARQUET, COMPRESSION SNAPPY);
    """)

    print("\n[SUCCESS] Pipeline Complete. Float64 Parquet files safely stored in 'data/processed/'")
    
    # --- Quick Sanity Check to prove the math ---
    print("\n" + "-"*80)
    print(" 🔍 GEOMETRY SANITY CHECK (v1_reserve_drain)")
    print("-" * 80)
    for domain, filepath, attack_key in [
        ("PAYMENTS", out_payments, "10.0.99.99"),
        ("BROKERAGE", out_brokerage, "WASH_TRADER_99"),
        ("AVIATION", out_aviation, "N999DL")
    ]:
        try:
            baseline_max = con.execute(f"SELECT MAX(v1_reserve_drain) FROM '{filepath}' WHERE link_key != '{attack_key}'").fetchone()[0]
            baseline_median = con.execute(f"SELECT MEDIAN(v1_reserve_drain) FROM '{filepath}' WHERE link_key != '{attack_key}'").fetchone()[0]
            print(f" {domain}: Organic Median = {baseline_median:.4f} | Organic Max = {baseline_max:.4f} | Attack Jitter = 0.90 - 1.00")
        except Exception as e:
            pass
    print("="*80 + "\n")

if __name__ == "__main__":
    t0 = time.time()
    run_etl_pipeline()
    print(f"Total Execution Time: {time.time() - t0:.2f} seconds")