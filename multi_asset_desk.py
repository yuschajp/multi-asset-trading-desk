import threading
import queue
import time
import random

# Multi-Asset Risk Profiles (Configured dynamically per asset class)
RISK_CONFIG = {
    "EQUITY": {"max_qty": 5000, "max_exposure": 500000},
    "FX":     {"max_qty": 1000000, "max_exposure": 10000000},
    "CRYPTO": {"max_qty": 10, "max_exposure": 700000}
}

class AdvancedRiskEngine:
    def __init__(self):
        self.positions = {"AAPL": 0, "EUR/USD": 0, "BTC/USD": 0}
        self.lock = threading.Lock() # Prevents race conditions across threads

    def validate_order(self, asset_class, ticker, qty, price):
        config = RISK_CONFIG.get(asset_class)
        if not config:
            print(f"[RISK REJECT] Unknown asset class: {asset_class}")
            return False

        notional_value = qty * price

        # Thread-safe risk parameter check
        with self.lock:
            # Check 1: Max Order Size
            if qty > config["max_qty"]:
                print(f"[RISK REJECT] {ticker} - Qty {qty} exceeds max limit of {config['max_qty']}")
                return False

            # Check 2: Max Exposure Limits
            current_exposure = self.positions[ticker] * price
            if current_exposure + notional_value > config["max_exposure"]:
                print(f"[RISK REJECT] {ticker} - Order violates max exposure limit of ${config['max_exposure']:,}")
                return False

            # Pre-approve and provisionally update position
            self.positions[ticker] += qty
            return True

def market_data_ingestor(order_queue, asset_class, ticker, price_base):
    """Simulates an incoming high-frequency order stream for a specific asset class."""
    while True:
        # Simulate random order arrivals
        time.sleep(random.uniform(0.3, 0.9))
        qty = random.randint(1, int(RISK_CONFIG[asset_class]["max_qty"] * 1.5))
        price = price_base + random.uniform(-0.5, 0.5)
        
        order_packet = {
            "asset_class": asset_class,
            "ticker": ticker,
            "qty": qty,
            "price": price,
            "timestamp": time.time()
        }
        order_queue.put(order_packet)

def execution_worker(order_queue, risk_engine):
    """The core engine matching and routing trades from the queue."""
    while True:
        order = order_queue.get()
        if order is None:
            break
            
        print(f"[OMS] Order Received: {order['ticker']} - {order['qty']} units")
        
        # Pass order through the risk check
        approved = risk_engine.validate_order(
            order['asset_class'], order['ticker'], order['qty'], order['price']
        )
        
        if approved:
            # Simulate a 10ms execution delay to a remote matching engine
            time.sleep(0.01)
            print(f"[EXEC FILLED] {order['ticker']} executed at ${order['price']:.4f}\n")
        else:
            print(f"[OMS OUTCOME] Order dropped due to risk breach.\n")
            
        order_queue.task_done()

if __name__ == "__main__":
    print("="*60)
    print("LAUNCHING ASYNCHRONOUS MULTI-ASSET TRADING DESK ENGINE")
    print("="*60)

    order_bus = queue.Queue()
    risk_gatekeeper = AdvancedRiskEngine()

    # Start the execution worker thread
    worker = threading.Thread(target=execution_worker, args=(order_bus, risk_gatekeeper), daemon=True)
    worker.start()

    # Launch isolated ingestion threads representing different exchange gateways
    threading.Thread(target=market_data_ingestor, args=(order_bus, "EQUITY", "AAPL", 185.00), daemon=True).start()
    threading.Thread(target=market_data_ingestor, args=(order_bus, "FX", "EUR/USD", 1.0850), daemon=True).start()
    threading.Thread(target=market_data_ingestor, args=(order_bus, "CRYPTO", "BTC/USD", 67000.00), daemon=True).start()

    # Let the simulation run for 10 seconds before shutting down cleanly
    time.sleep(10)
    print("SHUTTING DOWN ENGINE INTERFACES CLEANLY.")
