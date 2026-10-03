# 🌐 NexusRisk: Cross-Industry Anomaly Triage & Risk Architecture

**Architect:** Hon Seng Choi | Principal Quantitative Risk Architect  
**Domain:** Enterprise Anomaly Detection, Financial Operations, Link Analysis  
**Infrastructure:** DuckDB (Zero-Copy OLAP), Python, Isolation Forest, TreeSHAP  

---

> *"Mathematicians study algebraic structures from a general point of view, compare different structures, and find relationships between them... this abstraction and generalization might appear to be hopelessly impractical—but it is not!"*  
> — **Charles C. Pinter, *A Book of Abstract Algebra***

### The Executive Philosophy: The Universal Geometry of Risk
In Charles C. Pinter’s *A Book of Abstract Algebra*, he notes that mathematicians strip away surface-level details to reveal identical underlying structures. To an outsider, abstraction seems hopelessly impractical. To an engineer, it is an hyper-efficient way to scale.

**NexusRisk applies this mathematical philosophy to Enterprise Risk.** 

Every modern business screams for some mechanism of risk control. An industrial manufacturer uses time-series CUSUM to detect microscopic machine drift before printing defective microchips. Payment networks hunt for bust-out fraud. Multi-asset brokerages track toxic flow. Airlines track cascading delays. The industry jargon changes, but once you strip away the domain names, the underlying mathematical geometry of an anomaly is identical. 

Traditional supervised risk models rely on historical ground-truth labels (e.g., waiting 60 days for a credit card chargeback). This creates a structural blind spot. **NexusRisk** bypasses this latency trap. It is a plug-and-play, unsupervised Dual-Gate engine that maps streaming operational data into universal geometric signals, isolating zero-day anomalies across any industry without requiring a single historical label.

---

## 🏗️ The Paradigm Shift: Universal Schema Adapter

Large enterprises frequently suffocate under legacy monolithic tech debt because they hardcode risk models to specific silos. NexusRisk introduces **Functional Minimalism**. 

The pipeline strips away domain-specific jargon and maps massive, unstructured payloads into 5 universal behavioral vectors, allowing agile deployment across multiple business domains:

| Universal Vector | Mode 1: Payment Networks | Mode 2: Capital Markets | Mode 3: Aviation Ops |
| :--- | :--- | :--- | :--- |
| **v1: Reserve Drain** | Account balance emptied | Free margin consumed | Turnaround buffer exhausted |
| **v2: Record Mismatch** | Unfunded ledger overrun | Settlement gap | Scheduled vs. actual gap |
| **v3: Speed Z-Score** | Transfer velocity burst | Toxic order rate | Hub departure congestion |
| **v4: Chokepoint** | Instant cash-out rail | Linked arbitrage loop | Tight aircraft rotation |
| **v5: Magnitude vs Baseline**| Current Tx vs. 30-day Avg | Position size vs. baseline | Delay mins vs. route avg |

---

## 🔬 The Red-Team Methodology (Data Integrity)
To prove the engine's capability without violating operational security, NexusRisk employs a strict **Red-Teaming** methodology:

1. **The Organic Baseline (The Haystack):** We ingest over **167 million rows** of real-world, unmanipulated operational data via the Kaggle API (IEEE-CIS Fraud, Optiver L2 Order Books, U.S. DOT Aviation Delays). This provides authentic, messy, heavy-tailed background noise.
2. **The Synthetic Graft (The Needles):** We deterministically inject a coordinated zero-day attack (e.g., 5,000 bots maxing out their transactional limits). 
3. **The Mathematical Moat:** Because fraud is adversarial, attackers drain 100% of available limits. Because organic users behave naturally, their transaction sizes follow a heavy-tailed Pareto distribution. By applying an honest **Logarithmic Squashing** transformation in an out-of-core DuckDB pipeline, organic whales naturally decay, creating a pure "Geometric Moat" that the Machine Learning engine can easily slice through.

*(Note: Hardware is a solved problem; Architecture is not. The zero-copy SQL pipeline executed this feature engineering on 167 million rows out-of-core on local hardware in minutes, proving heavy-tailed data does not always require an expensive cloud cluster).*

---

## 🛡️ The Dual-Gate ML Engine (Results)

Unsupervised AI is brilliant at catching zero-day attacks, but it is dangerous without a safety net. In a 10-million transaction environment, a standard 5% False Positive rate means incorrectly freezing 500,000 legitimate customers. 

NexusRisk solves this using a decoupled **Two-Gate** system:
* **Gate 1 (Isolation Forest):** Successfully caught **~99.8%** of the injected zero-day attackers across all three industries by mapping the structural void between organic and adversarial geometry.
* **Gate 2 (Dynamic Cohort Sentinel):** Grouped the population into specific statistical micro-cohorts (Tiers). By evaluating flagged users strictly against the live Median Absolute Deviation (MAD) of their peers, Gate 2 **mathematically rescued ~99% of False Positives**, clearing legitimate users who simply drifted too close to the anomaly boundary.

**Performance Benchmarks:**
* *Payments:* **99.0%** False Positive Reduction (from 2,610 down to 26).
* *Brokerage:* **98.7%** False Positive Reduction (from 5,442 down to 71).
* *Aviation:* **100.0%** False Positive Reduction (from 2,650 down to 0).
* *Execution Speed:* Evaluated statelessly in **< 8.0 seconds** on local hardware.

---

## ⚖️ Model Risk Management (SR 11-7) & Compliance
Deep Learning is brilliant, but if you cannot explain exactly *why* you declined a transaction to a regulator, your model is a massive liability. 

NexusRisk explicitly rejects "Black Box" outputs. Every alert natively integrates **Exact TreeSHAP**. The system outputs a deterministic, additive feature attribution matrix that translates the anomaly into a plain-English After-Action Review (AAR):
> *"Primary Driver (60%): Reserve Drain ($95,000 withdrawn from a $100,000 balance)."*

---

## 🚀 Quick Start (Local Reproduction)

This repository is fully idempotent. You can reproduce the pipeline locally:

```bash
# 1. Clone the repository
git clone [https://github.com/honsengchoi1/NexusRisk_Link_Engine.git](https://github.com/honsengchoi1/NexusRisk_Link_Engine.git)
cd NexusRisk_Link_Engine

# 2. Install dependencies
pip install -r requirements.txt

# 3. Execute the 3-Module Pipeline
python src/01_download_baselines.py     # Module 01: Kaggle Ingestion
python src/02_duckdb_etl_pipeline.py    # Module 02: DuckDB Log-Squashing & Red-Teaming
python src/03_ml_risk_engine.py         # Module 03: Gate 1 & Gate 2 Triage execution