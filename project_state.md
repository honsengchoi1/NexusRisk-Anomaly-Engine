# 📊 NexusRisk: Project State & Working Memory

**Project:** NexusRisk (Cross-Industry Anomaly & Network Triage Engine)  
**Architect:** Hon Seng Choi | Principal Quantitative Risk Architect  
**Current Phase:** Stage 7 — V2 Pipeline Deployed, UI Finalized, Preparing for Launch.

---

## 🛡️ PERMANENT DIRECTIVES & CAREER STRATEGY
1. **Career Pivot & Positioning:** Position for Lead / Principal / IC or Director roles at enterprise firms (Stripe, Worldpay, Delta, Tier-1 Banks). Break out of being "FX landlocked" by demonstrating cross-industry domain authority.
2. **Pedagogical & Technical Dual-Purpose:** Architecture must be both enterprise-functional and educational for a diverse audience (recruiters, quants, engineering VPs).
3. **Literature-Backed Defense:** All domain claims (especially FX microstructure and fraud rings) must be protected by regulatory enforcement actions (CFTC, Dodd-Frank) or peer-reviewed literature.
4. **OPSEC Perimeter:** The Python detection engine and the exact mathematical threshold parameters for Gate 2 remain strictly closed-source to prevent Adversarial Evasion Attacks.
5. **Functional Minimalism (The Tech Stack):** DuckDB (Zero-copy OLAP) + Parquet (`float64`) + Scikit-Learn + Vanilla HTML5/D3.js (Zero Python backend) + TreeSHAP + Isolation Forest. Zero bloated monoliths.

---

## 1. Executive Overview
**NexusRisk** is a plug-and-play, real-time network anomaly triage engine. While **ExoRisk** models how *external* macroeconomic shocks impact credit portfolios, **NexusRisk** models how *internal* behavioral anomalies spread across connected networks (Payment Clearing, Capital Markets, and Aviation).

## 2. The 5 Universal Plain-English Risk Signals ($v_i$)
To achieve cross-industry extensibility, raw payloads are normalized into 5 universal behavioral vectors via the Schema Adapter:
1. **Reserve Drain:** How fast is the safety cushion disappearing?
2. **Record Mismatch:** Does the official record match reality (Unfunded Overrun)?
3. **Activity Speed Spike:** Is activity happening too fast for this time stratum?
4. **High-Risk Chokepoint:** Is this flowing through an irreversible bottleneck?
5. **Magnitude vs. Normal:** How big is this event compared to the baseline?

## 3. Data Engineering Strategy (The "Hybrid Red-Team" Approach)
Instead of relying on purely synthetic data generators (which are easily attacked in interviews), the pipeline utilizes **pure SQL determinism over real-world data**.
*   **The Baselines (Noise):** Automated Kaggle API extraction of gigabyte-scale, real-world datasets:
    *   *Payments:* IEEE-CIS Fraud Detection (`train_transaction.csv`).
    *   *Brokerage:* Optiver Realized Volatility L2 Limit Order Book (`book_train.parquet`).
    *   *Aviation:* U.S. DOT Flight Delays Mirror (`DelayedFlights.csv`).
*   **The Pipeline (DuckDB):** An out-of-core, columnar ETL pipeline reads the raw files, establishes organic background noise, and utilizes SQL `CASE` to deterministically inject highly targeted attack topologies (Bust-Outs, Toxic Arbitrage, Cascading Hub Delays).
*   **The Math (Log-Squashing):** Output is mathematically compressed via Logarithmic Squashing `LN(1+x)` to honestly model Pareto (heavy-tailed) distributions without using artificial hard-caps. This naturally creates a "Geometric Moat" (~0.88 max organic vs. 0.90+ attacks). Exported natively as `float64` `.parquet` feature matrices to prevent memory crashes.

## 4. Core ML Architecture (The Dual-Gate Sentinel)
* **Gate 1 (Triage <2ms):** Contextually Stratified Isolation Forest + TreeSHAP (Plain-English root cause percentage matrices).
* **Gate 2 (The False Positive Fix):** Proprietary Dynamic Contextual Sentinel. Evaluates flagged nodes against live, dynamically calibrated peer micro-cohorts, automatically rescuing >98% of False Positives.
* **Decoupled Exposure Engine (Conceptual Downstream):** 
  * *Payments (Fraud):* Deterministic Limit Summing (Adversaries max out limits).
  * *Markets/Airlines (Operations):* Monte Carlo VaR (Stochastic cascading delays).

## 5. Working Backwards Execution Roadmap
- [x] **Phase 0:** Define Brand, Signals, and Abstract Algebra Philosophy.
- [x] **Phase 1:** Purge V1 Tech Debt; Establish V2 Pristine Directory.
- [x] **Stage 2:** Data Engineering: Module 01 (Idempotent Kaggle API Downloader).
- [x] **Stage 3:** Data Engineering: Module 02 (Log-Squashing, Hybrid Grafts, float64 schema).
- [x] **Stage 4:** ML Core: Module 03 (Stateless iForest + Multi-Dimensional Gate 2).
- [x] **Stage 5:** Compliance: Module 04 (TreeSHAP Executive Translation).
- [x] **Stage 6:** Build Live-Streaming HTML/D3.js Visual Command Center (`ui/index.html`).
- [ ] **Stage 7:** Publish Executive Whitepaper and clean `README.md`.
- [ ] **Stage 8:** Launch LinkedIn 6-Part Drip Campaign & Direct Recruiter Outreach.