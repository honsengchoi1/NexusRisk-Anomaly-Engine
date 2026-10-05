# 📊 SR 11-7 Model Card: NexusRisk Dual-Gate Anomaly Engine

**Model Name:** NexusRisk Dual-Gate Triage Engine  
**Version:** 1.0 (Stateless Execution Architecture)  
**Architect:** Hon Seng Choi | Principal Quantitative Risk Architect  
**Model Type:** Unsupervised Spatial Outlier Detection (Isolation Forest) paired with Adaptive Contextual Validation.  

---

## 1. Intended Use & Executive Scope
*   **Primary Objective:** To perform cross-industry, day-zero anomaly detection without relying on historical, supervised training labels.
*   **Target Domains:** Payment Networks (Bust-Out/Fraud), Capital Markets (Toxic Flow/Arbitrage), and Aviation Logistics (Cascading Hub Delays).
*   **Out-of-Scope:** This model is not designed for natural language processing, credit underwriting, or long-term macroeconomic forecasting. It is strictly a behavioral geometry and event-triage engine.

---

## 2. Model Architecture & Pipeline Mechanics
*   **Data Ingestion & Feature Engineering:** Executes entirely out-of-core utilizing **DuckDB** (Zero-Copy OLAP).
*   **Dimensionality Reduction:** Raw tabular data is mapped into 5 universal behavioral vectors (Reserve Drain, Record Mismatch, Speed Z-Score, Chokepoint, Magnitude vs. Baseline).
*   **Variance Normalization:** To prevent Euclidean distance distortion caused by heavy-tailed (Pareto) distributions, all magnitude vectors undergo a Logarithmic Compression transform (`LN(1+x)`). This ensures extreme, legitimate corporate outliers do not mathematically blind the AI to micro-anomalies.
*   **Gate 1 (Isolation):** An unsupervised **Isolation Forest** evaluates the spatial geometry of the network to isolate zero-day vulnerabilities.
*   **Gate 2 (Validation):** An **Adaptive Contextual Thresholding** algorithm filters out macro-economic volume shocks (e.g., Black Friday sales, market flash-crashes) by evaluating Gate 1 anomalies strictly against the real-time median variance of their localized peer cohort.

---

## 3. Training & Evaluation Data (Red-Teaming)
Because zero-day anomalies lack historical labels by definition, the model's efficacy was verified utilizing a rigorous Red-Teaming methodology:

*   **The Organic Baseline (Background Noise):** The model evaluated **~167 million rows** of authentic, unmanipulated operational data to establish realistic, heavy-tailed background variance.
    *   *Payments:* IEEE-CIS Fraud Detection (~1M rows)
    *   *Brokerage:* Optiver L2 Order Books (~159M tick-level rows)
    *   *Aviation:* U.S. DOT Commercial Flight Logs (~7M rows)
*   **The Synthetic Injection (Target Vectors):** Highly coordinated, deterministic "Resource Exhaustion" attacks (e.g., coordinated limit-maxing) were synthetically injected into the baseline to simulate zero-day behavior. 

---

## 4. Quantitative Performance Metrics
The Dual-Gate architecture was evaluated on its ability to identify the synthetic attackers while minimizing operational friction (False Positives) on the organic baseline.

*   **Gate 1 (Detection Rate):** Successfully isolated **~99.8%** of synthetic zero-day injections across all three domains.
*   **Gate 2 (Friction Reduction):** 
    *   *Payments:* **99.0%** False Positive Reduction
    *   *Brokerage:* **98.7%** False Positive Reduction
    *   *Aviation:* **100.0%** False Positive Reduction
*   **Compute Efficiency:** The DuckDB ETL pipeline processed the 167-million-row payload locally out-of-core in **13.5 minutes**, proving highly efficient infrastructure optimization.

---

## 5. SR 11-7 Explainability & Transparency (FCRA Compliance)
To prevent the regulatory liabilities associated with "Black-Box" AI, the NexusRisk engine natively integrates **Exact TreeSHAP** (SHapley Additive exPlanations). 

The engine does not output opaque log-odds. Every flagged alert is mathematically deconstructed into an auditable feature attribution matrix, outputting a deterministic, plain-English root cause that sums exactly to 100% (e.g., *80.8% attributed to Reserve Drain, 5.5% attributed to Speed Z-Score*). This ensures total transparency for regulatory audits and Adverse Action notices.

---

## 6. Known Limitations & Trade-Offs
In accordance with MRM guidelines, the following architectural vulnerabilities and limitations must be monitored during production deployment:

1.  **The Cohort Cold-Start Problem:** Gate 2 requires a statistically significant micro-cohort to calculate a stable adaptive threshold. If a new operational product launches and a cohort has too few active participants, the variance becomes hyper-sensitive, temporarily inflating the false positive rate until the cohort matures.
2.  **Asynchronous Compute Overhead:** While the Isolation Forest scores network geometry in low milliseconds, calculating Exact TreeSHAP for regulatory explanation is computationally heavy. In ultra-high-frequency environments (e.g., sub-millisecond market arbitrage), SHAP calculation must be decoupled and processed asynchronously in a secondary queue so it does not block the primary transaction execution path.
3.  **OPSEC Constraints:** To prevent adversarial poisoning attacks, the exact parameters, dynamic look-back periods, and cohort definitions utilized in the Gate 2 filtering mechanism are deliberately decoupled from this public documentation.