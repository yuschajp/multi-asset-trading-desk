# Multi-Asset Trading Desk Engine & Pre-Trade Risk Ledger

A containerized, event-driven middle-office engineering framework written in Python 3.12 to simulate high-frequency institutional trade intake, multi-threaded exception management, and real-time risk controls.

## Business Problem Addressed
In institutional capital markets operations, managing concurrent trade feeds from fragmented execution gateways (Equities, FX, Crypto) introduces significant operational risk. Without strict concurrency controls, processing delays and race conditions can compromise book-of-record synchronization and allow catastrophic pre-trade risk breaches.

## Architecture & Technical Highlights
* **Asynchronous Concurrency:** Utilizes a multi-threaded Python architecture to process independent execution streams simultaneously.
* **Thread-Safe Risk Ledger:** Implements mutual exclusion locks (`threading.Lock`) to completely eliminate race conditions during real-time valuation updates and portfolio exposure checks.
* **Decoupled Telemetry Pipeline:** Forwards execution fills and data errors directly to standard output streams, allowing Linux terminal tools (`grep`, `awk`, `uniq`) to audit and aggregate desk exceptions dynamically.
* **Containerized Deployment:** Completely isolated via Docker to ensure deterministic performance across any cloud or local operating system infrastructure.
