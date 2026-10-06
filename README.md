# 🌐 NexusRisk: Cross-Industry Anomaly & Link Analysis Engine

**Architect:** Hon Seng Choi | Principal Quantitative Risk Architect  
**Target Scope:** Enterprise Anomaly Detection, Financial Operations, Link Analysis  
**Core Infrastructure:** DuckDB (Zero-Copy OLAP), Python, Isolation Forest, TreeSHAP, D3.js  

👉 [**View the Live Interactive Command Center HUD**](https://honsengchoi1.github.io/NexusRisk-Anomaly-Engine/ui/) 

---

## 🛡️ Operational Security (OPSEC) Disclaimer
> **Notice to Enterprise Architecture & Security Teams:** 
> To prevent adversarial evasion attacks and protect proprietary thresholding logic, the underlying Python ML inference engine, DuckDB pipeline mechanics, and dynamic Gate 2 parameters for this project are **strictly closed-source**. 
> 
> This repository serves as an Architectural Hub and UI Sandbox, containing the Executive Whitepaper, SR 11-7 Model Card, and the decoupled JSON-driven frontend presentation layer.

---

## 📌 Executive Summary

The primary objective of **NexusRisk** is to demonstrate that anomaly detection does not require domain-specific silos. Whether a business is tracking bust-out fraud on a payment network, toxic flow in a brokerage, or cascading delays at an aviation hub, the underlying mathematical geometry of the risk is identical.

A critical challenge in modern risk architecture is the "Zero-Day Blind Spot." Traditional supervised models (like XGBoost or Neural Networks) require historical ground-truth labels to learn. They force organizations to wait 60 days for a credit card chargeback or a settlement failure before training a model. By the time the AI learns to catch a novel attack vector, the financial damage is already done. 

NexusRisk bypasses this latency trap. It is a plug-and-play, dual-gate anomaly triage engine that normalizes massive streaming payloads into 5 universal behavioral vectors. By deploying an unsupervised Isolation Forest, the engine evaluates the spatial geometry of the network statelessly. Because it does not rely on history, it isolates zero-day anomalies across any industry on Day 1 without requiring a single historical label.

---

## 📖 Deep Dives & Core Documentation

For a comprehensive breakdown of the mathematical philosophy, the data pipeline, and the exact Model Risk Management (MRM) framework used, please refer to the core documentation:

*   **[The NexusRisk Business Whitepaper](docs/NexusRisk_Executive_Whitepaper.md)**
*   **[SR 11-7 Model Card & Regulatory Governance](docs/MODEL_CARD.md)**

---

## 🏗️ System Architecture & Data Evolution

The repository features a fully idempotent pipeline, transitioning 167 million rows of raw operational data into a production-grade inference application.

### 1. Idempotent ETL & Staging Layer
To prove the engine works against authentic noise, the pipeline ingests **167 million rows** of real, unmanipulated operational data via the Kaggle API (IEEE-CIS Fraud, Optiver L2 Order Books, U.S. DOT Aviation Delays).
*   **Logarithmic Vector Normalization:** Real-world enterprise data follows a heavy-tailed Pareto distribution. If scaled linearly, massive legitimate outliers (like a $50k corporate payroll) mathematically dominate the AI's variance calculations, blinding it to smaller anomalies. NexusRisk pushes a Logarithmic Compression transformation (`LN(1+x)`) directly into a zero-copy **DuckDB SQL pipeline**. This normalizes the feature space, allowing the AI to evaluate true behavioral geometry (like speed and magnitude) without being blinded by sheer size.
*   **Red-Teaming Injection:** The engine deterministically injects highly coordinated, synthetic zero-day attacks (e.g., Resource Exhaustion attacks) directly into the baselines to simulate novel, unseen threats.

### 2. Dual-Gate Unsupervised Inference Engine
*   **Gate 1 (Isolation Forest):** Scans the geometric void created by the DuckDB normalization layer, successfully trapping **~99.8%** of the injected zero-day attacks instantly.
*   **Gate 2 (False Positive Rescue):** Unsupervised AI inherently over-flags during macro volume surges. Flagged entities are routed through a secondary, proprietary contextual validation gate, mathematically rescuing **~98% to 100% of False Positives**.

### 3. Model Risk Management & Interpretability
Black-box AI is a regulatory liability. Every alert that survives Gate 2 natively integrates **Exact TreeSHAP** to output a deterministic, plain-English root cause matrix that strictly sums to 100%, enabling auditable, transparent adverse action notices.

```text
 ┌──────────────────────────────────────────────────────────────────────────────────┐
 │                     NEXUSRISK DUAL-GATE PIPELINE ARCHITECTURE                    │
 ├──────────────────────────────────────────────────────────────────────────────────┤
 │                                                                                  │
 │  [ THE ORGANIC BASELINE ]                 [ RED-TEAM INJECTION ]                 │
 │  ├── 167M+ Rows (Payments, Trading, Ops)  ├── Synthetic Zero-Day Anomalies       │
 │  └── Heavy-Tailed Pareto Distribution     └── Resource Exhaustion Attacks        │
 │                    │                                        │                    │
 │                    └──────────────────┬─────────────────────┘                    │
 │                                       ▼                                          │
 │  [ ZERO-COPY OLAP TRANSFORM ]                                                    │
 │  ├── DuckDB SQL Out-of-Core Execution                                            │
 │  ├── Domain-Agnostic Stripping (Mapping to 5 Universal Vectors)                  │
 │  └── Logarithmic Compression (LN(1+x)) to eliminate variance distortion          │
 │                                       │                                          │
 │                                       ▼                                          │
 │  [ DUAL-GATE ML INFERENCE ]                                                      │
 │  ├── Gate 1: Unsupervised Isolation Forest (Traps Zero-Day Vectors)              │
 │  ├── Gate 2: Adaptive Contextual Thresholding (Rescues 98%+ False Positives)     │
 │  └── SR 11-7 Compliance: Exact TreeSHAP Root Cause Extraction                    │
 │                                       │                                          │
 │                                       ▼                                          │
 │  [ HIGH-THROUGHPUT COMMAND CENTER ] (HTML5 / D3.js UI)                           │
 │  ├── Universal Cross-Domain Triage View                                          │
 │  ├── Deterministic SHAP Attribution Matrices                                     │
 │  └── Monte Carlo 1-Day Value at Risk (VaR) Exposure Calculation                  │
 │                                                                                  │
 └──────────────────────────────────────────────────────────────────────────────────┘
 ```
## 🔌 Enterprise Production Integration (Plug-and-Play)

Currently, this repository is configured as a decoupled prototype running locally via Python and DuckDB, exporting static JSON payloads to the frontend D3.js Command Center. 

To deploy this exact architecture into a live enterprise ecosystem (e.g., a commercial bank or airline), the core mathematical engine remains completely untouched. The ingestion and routing adapters are simply swapped:

*   **Swap the Ingestion Stream:** Instead of downloading static historical datasets, the DuckDB layer connects directly to the enterprise's live event streaming backbone (e.g., Apache Kafka, MQTT, or FIX protocol gateways).
*   **Containerize the Inference Engine:** The ML pipeline is wrapped in a stateless microservice (deployed via Docker) to mathematically score the live data stream in milliseconds.
*   **Live UI Broadcasting:** The static JSON handoff is replaced by an open WebSocket connection. As anomalies are scored, the TreeSHAP matrices and Monte Carlo VaR exposures are streamed in real-time directly to the risk desk dashboard without requiring browser refreshes.

---

## ⚠️ Architectural Limitations & Trade-Offs

No risk engine is a silver bullet. This architecture makes intentional engineering trade-offs:

1.  **Asynchronous Compute Overhead:** While the Isolation Forest scores network geometry in low milliseconds, calculating Exact TreeSHAP for regulatory explanation is computationally heavy. In ultra-high-frequency environments (e.g., sub-millisecond market arbitrage), SHAP calculation must be decoupled and processed asynchronously in a secondary queue so it does not block the primary transaction execution path.
