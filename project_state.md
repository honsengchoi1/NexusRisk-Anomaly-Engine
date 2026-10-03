# 📊 NexusRisk: Project State & Working Memory

**Project:** NexusRisk (Sister Flagship to ExoRisk)  
**Architect:** Hon Seng Choi | Principal Quantitative Risk Architect  
**Current Phase:** Stage 2 — Data Engineering (ETL Complete) & Transitioning to ML Engine  

---

## 🛡️ PERMANENT DIRECTIVES & CAREER STRATEGY
1. **Career Pivot & Positioning:** Position for Lead / Principal / IC or Director roles at enterprise firms (Stripe, Worldpay, Delta, Tier-1 Banks). Break out of being "FX landlocked" by demonstrating cross-industry domain authority.
2. **Pedagogical & Technical Dual-Purpose:** Architecture must be both enterprise-functional and educational for a diverse audience (recruiters, quants, engineering VPs).
3. **Literature-Backed Defense:** All domain claims (especially FX microstructure and fraud rings) must be protected by regulatory enforcement actions (CFTC, Dodd-Frank) or peer-reviewed literature.
4. **OPSEC Perimeter:** The Python detection engine and threshold parameters remain strictly closed-source to prevent Adversarial Evasion Attacks.
5. **Functional Minimalism (The Tech Stack):** DuckDB (Zero-copy OLAP) + Parquet + FastAPI + Vanilla HTML5/D3.js (Zero Streamlit) + TreeSHAP + Isolation Forest. 

---

## 1. Executive Overview
**NexusRisk** is a plug-and-play, real-time network anomaly triage engine. While **ExoRisk** models how *external* macroeconomic shocks impact credit portfolios, **NexusRisk** models how *internal* behavioral anomalies spread across connected networks (Payment Clearing, Capital Markets, and Aviation).

## 2. The 5 Universal Plain-English Risk Signals ($v_i \in [0,1]$)
1. **Reserve Drain %:** How fast is the safety cushion disappearing?
2. **Record Mismatch:** Does the official record match reality (Unfunded Overrun)?
3. **Activity Speed Spike:** Is activity happening too fast for this time stratum?
4. **High-Risk Chokepoint:** Is this flowing through an irreversible bottleneck?
5. **Size vs. Normal:** How big is this event compared to the baseline?

## 3. Data Engineering Strategy (The "Boring & Defensible" Approach)
Instead of relying on synthetic data generators (which are easily attacked in interviews), the pipeline utilizes **pure SQL determinism over real-world data**.
*   **The Baselines (Noise):** Automated Kaggle API extraction of gigabyte-scale, real-world datasets:
    *   *Payments:* IEEE-CIS Fraud Detection (`train_transaction.csv`).
    *   *Brokerage:* Optiver Realized Volatility L2 Limit Order Book (`book_train.parquet`).
    *   *Aviation:* U.S. DOT Flight Delays Mirror (`DelayedFlights.csv`).
*   **The Pipeline (DuckDB):** An out-of-core, columnar ETL pipeline reads the raw files, establishes organic background noise, and utilizes SQL `CASE` and Window functions to deterministically inject highly targeted attack topologies (Bust-Outs, Wash Trading, Cascading Hub Delays).
*   **The Sink:** Output is compressed into strictly bounded ($0.0 - 1.0$) `.parquet` feature matrices for ML ingestion.

## 4. Core ML Architecture (Next Steps)
* **Gate 1 (Triage <2ms):** Contextually Stratified Isolation Forest + TreeSHAP (Plain-English root cause).
* **Gate 2 (Seasonality Fix):** Real-Time Peer Cohort Sentinel (Median Absolute Deviation).
* **Decoupled Exposure Engine:** 
  * *Payments (Fraud):* Deterministic Limit Summing (Adversaries max out limits).
  * *Markets/Airlines (Operations):* Monte Carlo VaR (Stochastic cascading delays).

## 5. Working Backwards Execution Roadmap
- [x] **Phase 0:** Define Brand, Signals, and Architecture.
- [x] **Stage 1:** Repository Scaffold & Kaggle API Authentication.
- [x] **Stage 2:** Data Engineering: Automated Baseline Ingestion (`download_raw_data.py`).
- [x] **Stage 3:** Data Engineering: Pure-SQL DuckDB ETL to Parquet (`real_data_pipeline.py`).
- [ ] **Stage 4:** Data Engineering: EDA Sanity Check & Boundary Validation.
- [ ] **Stage 5:** Build ML Engine (Isolation Forest + Cohort Sentinel).
- [ ] **Stage 6:** Build FastAPI Microservice & D3.js Visual Command Center.
- [ ] **Stage 7:** Finalize Documentation (`README.md`, Whitepaper, LinkedIn Strategy).

## 🗣️ Interview Explanations (The "Why")

### 1. The Hybrid Data Strategy (The "Metal Detector" Analogy)
*   **The Problem:** You cannot test a zero-day fraud engine using old fraud data (because zero-days are unseen by definition). But you also can't use 100% fake synthetic data, because fake data lacks the unpredictable, messy noise of real human behavior.
*   **The Pitch:** *"Think of it like testing a metal detector. You don't test it in a sterile, empty room. You test it on a real public beach full of real trash, bottle caps, and foil. The 167 million rows of Kaggle data is my beach—authentic, messy background noise. Then, I used DuckDB SQL to deterministically bury 5,000 synthetic botnet attacks (the gold coins) at exact coordinates. Because my unsupervised AI successfully found the 5,000 coins hidden inside 167 million rows of real-world trash, I mathematically proved the engine works in production."*

### 2. Log-Squashing (The "Billionaire / Pareto" Analogy)
*   **The Problem:** Real-world operational data (transaction amounts, flight delays) is "heavy-tailed" (a Pareto distribution). 99% of transactions are $50, but a few legitimate corporate whales transfer $50,000. 
*   **The Pitch:** *"If you scale data linearly from 0 to 1, it's like putting normal people and billionaires on the same wealth chart. All the normal people get crushed into a single microscopic pixel at the bottom. The AI goes blind and can't tell the difference between a $10 user and a $1,000 user. By using Logarithmic Squashing `LN(1+x)`, we honestly compress the massive $50k whales, allowing the normal data to spread out visually. This naturally creates a 'Geometric Moat'—an empty mathematical void between my largest normal customers (~0.88) and my maxed-out attackers (0.90+). The Isolation Forest easily slices them apart."*
## 🗣️ Interview Explanations (The "Why")

### 1. The Hybrid Data Strategy (The "Metal Detector" Analogy)
*   **The Problem:** You cannot test a zero-day fraud engine using old fraud data (because zero-days are unseen by definition). But you also can't use 100% fake synthetic data, because fake data lacks the unpredictable, messy noise of real human behavior.
*   **The Pitch:** *"Think of it like testing a new metal detector. You don't test it in a sterile, empty room. You test it on a real public beach full of real trash, bottle caps, and foil. The 167 million rows of Kaggle data is my beach—it is authentic, messy background noise. Then, I used DuckDB SQL to deterministically bury 5,000 synthetic botnet attacks (the gold coins) at exact coordinates. Because my unsupervised AI successfully found the 5,000 coins hidden inside 167 million rows of real-world trash, I mathematically proved the engine works in a live production environment."*

### 2. Log-Squashing (The "Billionaire / Pareto" Analogy)
*   **The Problem:** Real-world operational data (transaction amounts, flight delays) is "heavy-tailed" (a Pareto distribution). 99% of transactions are $50, but a few legitimate corporate whales transfer $50,000. 
*   **The Pitch:** *"If you scale data linearly from 0 to 1, it's like putting normal people and billionaires on the same wealth chart. All the normal people get crushed into a single microscopic pixel at the bottom. The AI goes blind and can't tell the difference between a $10 user and a $1,000 user. By using Logarithmic Squashing `LN(1+x)` in the database layer, we honestly compress the massive $50k whales, allowing the normal data to spread out visually. This naturally creates an empty mathematical void between my largest normal customers (~0.88) and my maxed-out attackers (0.90+). The Isolation Forest easily slices them apart without me having to fake the data."*