"""
NEXUSRISK V2: Stateless ML Risk Engine & Exposure Calculator (Module 03)
Ingests mathematically pure Parquet geometries. 
Executes Gate 1 (Isolation Forest) and Gate 2 (Dynamic Contextual Thresholding).
Triggers Decoupled Exposure Engine (Monte Carlo VaR) using Lazy Execution.
"""
import os
import duckdb
import pandas as pd
import numpy as np
import time
import json
from sklearn.ensemble import IsolationForest
import warnings

pd.options.mode.chained_assignment = None 
warnings.filterwarnings("ignore")

def run_ml_risk_engine():
    print("\n" + "="*85)
    print(" 🧠 NEXUSRISK V2: DUAL-GATE ML & EXPOSURE ENGINE (MODULE 03)")
    print("="*85)

    datasets = {
        "PAYMENTS": {"file": "data/processed/payments_vectors.parquet", "key": "10.0.99.99"},
        "BROKERAGE": {"file": "data/processed/brokerage_vectors.parquet", "key": "WASH_TRADER_99"},
        "AVIATION": {"file": "data/processed/aviation_vectors.parquet", "key": "N999DL"}
    }

    con = duckdb.connect()
    features = ['v1_reserve_drain', 'v2_record_mismatch', 'v3_speed_zscore', 'v4_chokepoint', 'v5_magnitude_vs_baseline']
    
    # Dictionary to hold the live exposure data for the UI
    live_exposure_payload = {}

    for domain, info in datasets.items():
        filepath = info["file"]
        attack_key = info["key"]
        
        if not os.path.exists(filepath):
            print(f"\n[!] Missing data for {domain}. Run Module 02 first.")
            continue
            
        print(f"\n--- 📊 DOMAIN: {domain} ---")
        t0 = time.time()
        
        # 1. STATELESS INGESTION
        query = f"""
            WITH 
            attack_data AS (SELECT * FROM '{filepath}' WHERE link_key = '{attack_key}'),
            organic_data AS (SELECT * FROM '{filepath}' WHERE link_key != '{attack_key}' USING SAMPLE 50000)
            SELECT * FROM attack_data UNION ALL SELECT * FROM organic_data
        """
        df = con.execute(query).df()
        is_attacker = df['link_key'] == attack_key
        total_attackers = is_attacker.sum()

        # 2. GATE 1: UNSUPERVISED TRIAGE (ISOLATION FOREST)
        X = df[features]
        model = IsolationForest(n_estimators=100, max_samples=256, random_state=42, n_jobs=-1)
        model.fit(X)
        
        raw_scores = model.decision_function(X)
        df['risk_score'] = (((raw_scores.max() - raw_scores) / (raw_scores.max() - raw_scores.min())) * 100).round(2)
        df['gate1_alert'] = df['risk_score'] >= 50
        
        gate1_attackers_caught = len(df[(df['gate1_alert'] == True) & is_attacker])
        gate1_fps_generated = len(df[(df['gate1_alert'] == True) & ~is_attacker])
        
        print(f"  [Gate 1] Unsupervised Triage: Caught {gate1_attackers_caught}/{total_attackers} | FPs: {gate1_fps_generated}")

        # 3. METADATA ROUTING
        df['v1_noisy'] = df['v1_reserve_drain'] + np.random.normal(0, 1e-6, len(df))
        try:
            df['micro_cohort'] = pd.qcut(df['v1_noisy'], q=4, labels=['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum'])
        except ValueError:
            df['micro_cohort'] = pd.cut(df['v1_noisy'], bins=4, labels=['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum'])
        
        # 4. GATE 2: CONTEXTUAL THRESHOLDING
        gate1_flagged = df[df['gate1_alert'] == True].copy()
        gate1_cleared = df[df['gate1_alert'] == False].copy()
        
        final_fp_count = 0
        final_attackers_count = 0
        
        confirmed_anomalies_list = []
        
        for cohort in ['Tier_Standard', 'Tier_Silver', 'Tier_Gold', 'Tier_Platinum']:
            cohort_cleared = gate1_cleared[gate1_cleared['micro_cohort'] == cohort]
            cohort_flagged = gate1_flagged[gate1_flagged['micro_cohort'] == cohort].copy()
            
            if len(cohort_cleared) == 0: continue
            
            if len(cohort_flagged) > 0:
                max_mad_distance = pd.Series(0.0, index=cohort_flagged.index)
                for v in ['v1_reserve_drain', 'v2_record_mismatch', 'v3_speed_zscore', 'v5_magnitude_vs_baseline']:
                    v_baseline = cohort_cleared[v]
                    v_mad = (v_baseline - v_baseline.median()).abs().median() + 0.001
                    v_dist = (cohort_flagged[v] - v_baseline.median()).abs() / v_mad
                    max_mad_distance = np.maximum(max_mad_distance, v_dist)
                
                cohort_flagged['gate2_confirmed'] = max_mad_distance > 10
                final_attackers_count += len(cohort_flagged[(cohort_flagged['link_key'] == attack_key) & (cohort_flagged['gate2_confirmed'] == True)])
                final_fp_count += len(cohort_flagged[(cohort_flagged['link_key'] != attack_key) & (cohort_flagged['gate2_confirmed'] == True)])
                
                confirmed_anomalies_list.append(cohort_flagged[cohort_flagged['gate2_confirmed'] == True])

        print(f"  [Gate 2] Dynamic Thresholding: Rescued {gate1_fps_generated - final_fp_count} FPs | Final Target Lock: {final_attackers_count}")
        
        # ---------------------------------------------------------
        # 5. DECOUPLED EXPOSURE ENGINE (Lazy Execution)
        # ---------------------------------------------------------
        print(f"  [Exposure Engine] Calculating Financial Blast Radius...")
        
        confirmed_df = pd.concat(confirmed_anomalies_list) if confirmed_anomalies_list else pd.DataFrame()
        attacker_nodes = confirmed_df[confirmed_df['link_key'] == attack_key]
        
        if not attacker_nodes.empty:
            target = attacker_nodes.iloc[0]
            np.random.seed(42) # Deterministic for UI consistency
            
            if domain == "PAYMENTS":
                # Deterministic Limit Summing (Retail/SMB Bust-Out)
                limit = 150000 
                loss = target['v1_reserve_drain'] * limit
                exposure_val = f"${loss:,.0f}"
                exposure_label = "1-Day Capital Risk"

            elif domain == "BROKERAGE":
                # Stochastic Monte Carlo VaR (1-Day Liquidity Risk)
                paths = np.random.normal(0, 0.22 / np.sqrt(252), (10000, 1))
                var_99 = np.percentile(np.exp(np.cumsum(paths, axis=1))[:, -1] - 1, 1) * 10000000
                exposure_val = f"${abs(int(var_99)):,}"
                exposure_label = "1-Day Capital Risk"

            elif domain == "AVIATION":
                # Stochastic Monte Carlo VaR (Cascading Flight Delays) - 1 Day Horizon
                cascading_delay = np.random.lognormal(mean=4.5, sigma=0.8, size=10000)
                p95_delay = np.percentile(cascading_delay, 95)
                exposure_val = f"{int(p95_delay)} Mins"
                exposure_label = "1-Day Delay Risk"

            print(f"   -> {exposure_label}: {exposure_val}")
            
            live_exposure_payload[domain] = {
                "value": exposure_val,
                "label": exposure_label
            }

        print(f"  Domain processed in {time.time()-t0:.2f}s")
    
    # 6. EXPORT PAYLOAD TO UI
    os.makedirs('ui', exist_ok=True)
    with open('ui/live_exposure.js', 'w') as f:
        f.write(f"const liveExposure = {json.dumps(live_exposure_payload, indent=4)};")
    print(" [✓] Live Exposure Payload exported successfully to ui/live_exposure.js\n")

if __name__ == "__main__":
    t0 = time.time()
    run_ml_risk_engine()
    print(f"Total Execution Time: {time.time() - t0:.2f} seconds")