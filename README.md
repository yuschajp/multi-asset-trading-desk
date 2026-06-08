# Multi-Asset Trading Desk Engine & Pre-Trade Risk Ledger

A containerized, event-driven middle-office engineering framework written in Python 3.12 to simulate high-frequency institutional trade intake, multi-threaded exception management, and real-time risk controls.

## Business Problem Addressed
In institutional capital markets operations, managing concurrent trade feeds from fragmented execution gateways (Equities, FX, Crypto) introduces significant operational risk. Without strict concurrency controls, processing delays and race conditions can compromise book-of-record synchronization and allow catastrophic pre-trade risk breaches.

## Architecture & Technical Highlights
* **Asynchronous Concurrency:** Utilizes a multi-threaded Python architecture to process independent execution streams simultaneously.
* **Thread-Safe Risk Ledger:** Implements mutual exclusion locks (`threading.Lock`) to completely eliminate race conditions during real-time valuation updates and portfolio exposure checks.
* **Decoupled Telemetry Pipeline:** Forwards execution fills and data errors directly to standard output streams, allowing Linux terminal tools (`grep`, `awk`, `uniq`) to audit and aggregate desk exceptions dynamically.
* **Containerized Deployment:** Completely isolated via Docker to ensure deterministic performance across any cloud or local operating system infrastructure.

## 🏗️ Core Engine Architecture

```mermaid
graph TD
    %% Define Styles
    classDef client fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef engine fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef lock fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef gateway fill:#e8f5e9,stroke:#388e3c,stroke-width:1px;

    %% Workflow Nodes
    A[Concurrent Client Order Ingestion] --> B(Async Execution Gateway)
    
    subgraph "Event-Driven Order Processing Engine"
        B --> C{Order Validation}
        C -- Invalid Parameters --> D[Status: REJECTED]
        C -- Valid Parameters --> E(Acquire threading.Lock)
        
        subgraph "Thread-Safe Critical Section"
            E --> F[Mutex Lock Engaged]
            F --> G{Pre-Trade Risk Exposure Check}
            G -- Exceeds Threshold --> H[Status: RISK_VIOLATION / Release Lock]
            G -- Within Threshold --> I[Update Real-Time Risk Ledger / Balance State]
        end
    end
    
    I --> J(Release threading.Lock)
    J --> K[Format Fix Execution Message]
    
    subgraph "Institutional Execution Gateways"
        K --> L[(Equity Gateways)]
        K --> M[(Fixed Income Gateways)]
    end

    %% Apply Styles
    class A client;
    class B,C,D,K engine;
    class E,F,G,H,I,J lock;
    class L,M gateway;
