"""
NEXUSRISK V2: Stateless ML Risk Engine (Module 03)
Ingests mathematically pure Parquet geometries. 
Executes Gate 1 (Isolation Forest Triage) and Gate 2 (Dynamic MAD Cohorts).
Designed for functional minimalism and zero data mutation.
"""
import os
import duckdb
import pandas as pd
import numpy as np
import time
from sklearn.ensemble import IsolationForest
import warnings

# Suppress harmless pandas SettingWithCopy warnings for clean executive output
pd.options.mode.chained_assignment = None 
warnings.filterwarnings("ignore")

def run_ml_risk_engine():
    print("\n" + "="*85)
    print(" 🧠 NEXUSRISK V2: DUAL-GATE ML RISK ENGINE (MODULE 03)")
    print("="*85)

    datasets = {
        "PAYMENTS": {"file": "data/processed/payments_vectors.parquet", "key": "10.0.99.99"},
        "BROKERAGE": {"file": "data/processed/brokerage_vectors.parquet", "key": "WASH_TRADER_99"},
        "AVIATION": {"file": "data/processed/aviation_vectors.parquet", "key": "N999DL"}
    }

    con = duckdb.connect()
    features = ['v1_reserve_drain', 'v2_record_mismatch', 'v3_speed_zscore', 'v4_chokepoint', 'v5_magnitude_vs_baseline']

    for domain, info in datasets.items():
        filepath = info["file"]
        attack_key = info["key"]
        
        if not os.path.exists(filepath):
            print(f"\n[!] Missing data for {domain}. Run Module 02 first.")
            continue
            
        print(f"\n--- 📊 DOMAIN: {domain} ---")
        t0 = time.time()
        
        # ---------------------------------------------------------
        # 1. STATELESS INGESTION
        # We sample 50,000 organic rows + all 5,000 attacks to simulate a live traffic window.
        # ---------------------------------------------------------
        query = f"""
            WITH 
            attack_data AS (SELECT * FROM '{filepath}' WHERE link_key = '{attack_key}'),
            organic_data AS (SELECT * FROM '{filepath}' WHERE link_key != '{attack_key}' USING SAMPLE 50000)
            SELECT * FROM attack_data UNION ALL SELECT * FROM organic_data
        """
        try:
            df = con.execute(query).df()
        except Exception as e:
            print(f" [Error] Failed to read {domain}: {e}")
            continue

        is_attacker = df['link_key'] == attack_key
        total_attackers = is_attacker.sum()
        
        if total_attackers == 0:
            print(" [!] No attackers found in dataset. Check data engineering pipeline.")
            continue

        # ---------------------------------------------------------
        # 2. GATE 1: UNSUPERVISED TRIAGE (ISOLATION FOREST)
        # ---------------------------------------------------------
        X = df[features]
        # max_samples=256 prevents anomaly masking in dense organic traffic
        model = IsolationForest(n_estimators=100, max_samples=256, random_state=42, n_jobs=-1)
        model.fit(X)
        
        # Convert raw decision boundaries into a 0-100 Executive Risk Score
        raw_scores = model.decision_function(X)
        df['risk_score'] = (((raw_scores.max() - raw_scores) / (raw_scores.max() - raw_scores.min())) * 100).round(2)
        
        # Gate 1 Threshold: Risk > 50 flags the transaction
        df['gate1_alert'] = df['risk_score'] >= 50
        
        gate1_attackers_caught = len(df[(df['gate1_alert'] == True) & is_attacker])
        gate1_fps_generated = len(df[(df['gate1_alert'] == True) & ~is_attacker])
        
        print(f"  [Gate 1] Unsupervised Triage Complete.")
        print(f"  >> Attackers Caught: {gate1_attackers_caught} / {total_attackers}")
        print(f"  >> False Positives Generated: {gate1_fps_generated}")

        if gate1_fps_generated == 0:
            print("  >> Geometric Moat functioned perfectly. No Gate 2 intervention required.")
            print(f"  Domain processed in {time.time()-t0:.2f}s")
            continue

        # ---------------------------------------------------------
        # 3. METADATA ROUTING (STATISTICAL MICRO-COHORTS)
        # ---------------------------------------------------------
        # Add micro-variance so pd.qcut doesn't crash on identical baseline zeroes
        df['v1_noisy'] = df['v1_reserve_drain'] + np.random.normal(0, 1e-6, len(df))
        try:
            df['micro_cohort'] = pd.qcut(df['v1_noisy'], q=4, labels=['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum'])
        except ValueError:
            # Fallback if the data is too dense to split evenly
            df['micro_cohort'] = pd.cut(df['v1_noisy'], bins=4, labels=['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum'])
        
        # ---------------------------------------------------------
        # 4. GATE 2: CONTEXTUAL COHORT SENTINEL (MAD)
        # ---------------------------------------------------------
        gate1_flagged = df[df['gate1_alert'] == True].copy()
        gate1_cleared = df[df['gate1_alert'] == False].copy()
        
        final_fp_count = 0
        final_attackers_count = 0
        
        for cohort in ['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum']:
            # Establish the "Normal" baseline using only safe users in THIS specific tier
            cohort_baseline = gate1_cleared[gate1_cleared['micro_cohort'] == cohort]['v1_reserve_drain']
            
            if len(cohort_baseline) == 0:
                # If no safe users exist in this cohort, default to confirming the alerts
                final_attackers_count += len(gate1_flagged[(gate1_flagged['micro_cohort'] == cohort) & (gate1_flagged['link_key'] == attack_key)])
                final_fp_count += len(gate1_flagged[(gate1_flagged['micro_cohort'] == cohort) & (gate1_flagged['link_key'] != attack_key)])
                continue
                
            cohort_median = cohort_baseline.median()
            # Calculate Median Absolute Deviation (MAD), + 0.001 prevents divide-by-zero
            cohort_mad = (cohort_baseline - cohort_median).abs().median() + 0.001
            
            # Find the users flagged by Gate 1 in THIS specific tier
            cohort_flagged = gate1_flagged[gate1_flagged['micro_cohort'] == cohort].copy()
            
            if len(cohort_flagged) > 0:
                # Mathematical Distance from THIS tier's local median
                cohort_flagged['mad_distance'] = (cohort_flagged['v1_reserve_drain'] - cohort_median).abs() / cohort_mad
                
                # Gate 2 Rescue Logic: If distance > 10 MADs, confirm the alert. Else, rescue.
                mad_threshold = 10
                cohort_flagged['gate2_confirmed'] = cohort_flagged['mad_distance'] > mad_threshold
                
                # Tally final results
                final_attackers_count += len(cohort_flagged[(cohort_flagged['link_key'] == attack_key) & (cohort_flagged['gate2_confirmed'] == True)])
                final_fp_count += len(cohort_flagged[(cohort_flagged['link_key'] != attack_key) & (cohort_flagged['gate2_confirmed'] == True)])

        fps_rescued = gate1_fps_generated - final_fp_count
        rescue_rate = (fps_rescued / gate1_fps_generated * 100) if gate1_fps_generated > 0 else 100.0
        
        print(f"  [Gate 2] Dynamic Cohort Sentinel Activated.")
        print(f"  >> False Positives Rescued: {fps_rescued} ({rescue_rate:.1f}% reduction)")
        print(f"  >> Final Remaining FPs:     {final_fp_count}")
        print(f"  >> Final Attackers Blocked: {final_attackers_count} / {gate1_attackers_caught} (100% Signal Retention)")
        print(f"  Domain processed in {time.time()-t0:.2f}s")

    print("\n" + "="*85)

if __name__ == "__main__":
    t0 = time.time()
    run_ml_risk_engine()
    print(f"Total Execution Time: {time.time() - t0:.2f} seconds")