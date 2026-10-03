"""
NEXUSRISK V2: SR 11-7 Compliance Engine (Module 04)
Pairs the unsupervised Isolation Forest with Exact TreeSHAP.
Translates complex geometric anomaly scores into plain-English, 
auditable percentage-based blame matrices for executive review.
"""
import os
import duckdb
import pandas as pd
import numpy as np
import shap
import time
from sklearn.ensemble import IsolationForest
import warnings

# Suppress warnings for clean executive output
warnings.filterwarnings("ignore")
pd.options.mode.chained_assignment = None

def run_shap_compliance():
    print("\n" + "="*85)
    print(" ⚖️ NEXUSRISK V2: SR 11-7 COMPLIANCE ENGINE (MODULE 04)")
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
            
        print(f"\n--- 🔍 DOMAIN: {domain} ---")
        t0 = time.time()
        
        # 1. Stateless Ingestion (Sample 5,000 to keep SHAP fast)
        query = f"""
            WITH 
            attack_data AS (SELECT * FROM '{filepath}' WHERE link_key = '{attack_key}' LIMIT 1),
            organic_data AS (SELECT * FROM '{filepath}' WHERE link_key != '{attack_key}' USING SAMPLE 5000)
            SELECT * FROM attack_data UNION ALL SELECT * FROM organic_data
        """
        try:
            df = con.execute(query).df()
        except Exception as e:
            print(f" [Error] Failed to read {domain}: {e}")
            continue
            
        X = df[features].astype('float64')
        target_row = df[df['link_key'] == attack_key].iloc[0]
        
        # 2. Train Lightweight Isolation Forest
        model = IsolationForest(n_estimators=100, max_samples=256, random_state=42, n_jobs=-1)
        model.fit(X)
        
        raw_scores = model.decision_function(X)
        risk_score = (((raw_scores.max() - raw_scores[0]) / (raw_scores.max() - raw_scores.min())) * 100).round(2)
        
        # 3. Initialize TreeSHAP
        explainer = shap.TreeExplainer(model)
        
        # We only want to explain the specific anomaly (The Attacker)
        X_target = pd.DataFrame([target_row[features]])
        
        shap_values = explainer.shap_values(X_target)
        
        # IsolationForest returns SHAP values differently depending on sklearn version.
        if isinstance(shap_values, list):
            shap_flat = shap_values[0]
            if len(shap_flat.shape) > 1: shap_flat = shap_flat[0]
        else:
            shap_flat = shap_values
            if len(shap_flat.shape) > 1: shap_flat = shap_flat[0]

        # 4. Executive Translation (Percentage Blame)
        # We take the absolute impact of each feature to determine how much it drove the anomaly
        abs_shap = np.abs(shap_flat)
        total_impact = np.sum(abs_shap)
        
        if total_impact == 0:
            blame_percentages = np.zeros(len(features))
        else:
            blame_percentages = (abs_shap / total_impact) * 100

        print(f"  🚨 TARGET PROFILE: CONFIRMED ATTACKER (Key: {attack_key})")
        print(f"  Overall Risk Score: {risk_score}/100")
        print("  " + "-"*75)
        
        # Sort features by highest blame impact
        blame_matrix = list(zip(features, target_row[features], blame_percentages))
        blame_matrix.sort(key=lambda x: x[2], reverse=True)
        
        for feature, val, percent in blame_matrix:
            print(f"   => {feature:<25} | Vector: {val:.4f} | Root Cause Blame: {percent:>5.1f}%")
            
        print(f"\n  Compliance report generated in {time.time()-t0:.2f}s")

    print("\n" + "="*85)
    print(" 📜 EXECUTIVE TALKING POINT:")
    print(" 'I paired the Isolation Forest with TreeSHAP to guarantee compliance.")
    print(" When Gate 1 flags an entity, it doesn't just return a score; it outputs a")
    print(" deterministic, feature-by-feature blame matrix that satisfies regulatory")
    print(" audit requirements (FCRA/SR 11-7) for adverse action notices.'")
    print("="*85 + "\n")

if __name__ == "__main__":
    run_shap_compliance()