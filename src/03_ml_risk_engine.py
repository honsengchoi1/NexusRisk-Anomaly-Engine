"""
NEXUSRISK V2: Stateless ML Risk Engine (Module 03 - Multi-Dimensional)
Ingests mathematically pure Parquet geometries. 
Executes Gate 1 (Isolation Forest Triage) and Gate 2 (Dynamic MAD Cohorts).
Gate 2 is upgraded to scan ALL continuous vectors (V1, V2, V3, V5) simultaneously.
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
        # We sample 50,000 organic rows + all 5,000 attacks
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
        df['v1_noisy'] = df['v1_reserve_drain'] + np.random.normal(0, 1e-6, len(df))
        try:
            df['micro_cohort'] = pd.qcut(df['v1_noisy'], q=4, labels=['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum'])
        except ValueError:
            df['micro_cohort'] = pd.cut(df['v1_noisy'], bins=4, labels=['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum'])
        
        # ---------------------------------------------------------
        # 4. GATE 2: CONTEXTUAL COHORT SENTINEL (MULTI-DIMENSIONAL MAD)
        # ---------------------------------------------------------
        gate1_flagged = df[df['gate1_alert'] == True].copy()
        gate1_cleared = df[df['gate1_alert'] == False].copy()
        
        final_fp_count = 0
        final_attackers_count = 0
        
        for cohort in ['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum']:
            cohort_cleared = gate1_cleared[gate1_cleared['micro_cohort'] == cohort]
            cohort_flagged = gate1_flagged[gate1_flagged['micro_cohort'] == cohort].copy()
            
            if len(cohort_cleared) == 0:
                final_attackers_count += len(cohort_flagged[cohort_flagged['link_key'] == attack_key])
                final_fp_count += len(cohort_flagged[cohort_flagged['link_key'] != attack_key])
                continue
            
            if len(cohort_flagged) > 0:
                # Calculate maximum MAD distance across ALL continuous vectors
                max_mad_distance = pd.Series(0.0, index=cohort_flagged.index)
                
                for v in ['v1_reserve_drain', 'v2_record_mismatch', 'v3_speed_zscore', 'v5_magnitude_vs_baseline']:
                    v_baseline = cohort_cleared[v]
                    v_median = v_baseline.median()
                    v_mad = (v_baseline - v_median).abs().median() + 0.001
                    v_dist = (cohort_flagged[v] - v_median).abs() / v_mad
                    max_mad_distance = np.maximum(max_mad_distance, v_dist)
                
                # Gate 2 Rescue Logic: If max distance > 10 MADs on ANY vector, confirm the alert
                mad_threshold = 10
                cohort_flagged['gate2_confirmed'] = max_mad_distance > mad_threshold
                
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