import time
import random
import sys

# Define pre-trade risk limits (The Risk Ledger)
MAX_ORDER_SIZE = 5000       # Maximum shares per single order
MAX_POSITION_LIMIT = 20000  # Total maximum exposure across a single ticker

class TradingDesk:
    def __init__(self, ticker):
        self.ticker = ticker
        self.current_position = 0

    def check_pre_trade_risk(self, quantity, price):
        """Simulates an institutional pre-trade compliance gatekeeper."""
        print(f"[RISK] Evaluating Order: BUY {quantity} {self.ticker} @ ${price:.2f}")
        
        # Check 1: Single Order Quantity Limit (Fat-finger protection)
        if quantity > MAX_ORDER_SIZE:
            print(f"[REJECTED] Order size {quantity} exceeds Max Limit of {MAX_ORDER_SIZE}!")
            return False
            
        # Check 2: Total Exposure / Position Limit Check
        if self.current_position + quantity > MAX_POSITION_LIMIT:
            print(f"[REJECTED] Order would violate total position limit of {MAX_POSITION_LIMIT}!")
            return False
            
        return True

    def execute_order(self, quantity, price):
        """Routes the order to the mock exchange if risk approval is granted."""
        if self.check_pre_trade_risk(quantity, price):
            # Simulate network latency/execution fill
            time.sleep(0.05) 
            self.current_position += quantity
            print(f"[FILLED] Successfully executed BUY {quantity} {self.ticker} at ${price:.2f}")
            print(f"[POSITION] Current Net Position: {self.current_position} shares\n")
        else:
            print("[OMS] Order suppressed by compliance layer.\n")

# Run the live desk loop
if __name__ == "__main__":
    print("="*50)
    print("INITIALIZING MULTI-ASSET AUTOMATED DESK...")
    print("="*50)
    
    desk = TradingDesk("AAPL")
    
    # Mock data stream generating a mix of valid and high-risk orders
    mock_order_stream = [
        (2000, 185.50),   # Normal Order
        (6500, 185.60),   # Fat-finger violation (Too large)
        (4500, 185.75),   # Normal Order
        (15000, 185.90)   # Position Limit violation
    ]
    
    for qty, px in mock_order_stream:
        time.sleep(1) # Interval between market events
        desk.execute_order(qty, px)
