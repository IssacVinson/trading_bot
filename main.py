# main.py

import time
from datetime import datetime, timedelta
from ipo_schedule import get_upcoming_ipos
from mock_broker import MockBroker

# Use dependency injection later to swap in WebullBroker
broker = MockBroker(starting_balance=100000)

def run_bot():
    print("🔁 Starting IPO strategy engine...\n")
    ipos = get_upcoming_ipos()

    for ipo in ipos:
        symbol = ipo["symbol"]
        launch_dt = ipo["datetime"]

        # Step 1: Wait for IPO launch
        while datetime.now() < launch_dt:
            time_to_open = (launch_dt - datetime.now()).total_seconds()
            print(f"⏳ Waiting for {symbol} IPO at {launch_dt} ({round(time_to_open/60)} min left)...")
            time.sleep(min(60, time_to_open))  # Wait in 1-min chunks

        # Step 2: Simulate buying at market open
        market_price = broker.get_price(symbol)
        shares = int(broker.get_balance() // market_price)
        if shares == 0:
            print("⚠️ Not enough funds to purchase any shares.")
            continue

        avg_fill = broker.buy(symbol, shares, market_price)
        print(f"✅ Order filled @ ${avg_fill:.2f} for {shares} shares of {symbol}")

        entry_time = datetime.now()
        entry_price = avg_fill
        target_price = round(entry_price * 1.10, 2)
        print(f"🎯 Target price is ${target_price:.2f}. Monitoring...\n")

        # Step 3: Monitor price every minute
        while True:
            now = datetime.now()
            current_price = broker.get_price(symbol)

            # Exit if +10% hit
            if current_price >= target_price:
                proceeds = broker.sell(symbol, shares, current_price)
                print(f"💰 Sold {shares} shares @ ${current_price:.2f}, proceeds: ${proceeds:,.2f}")
                break

            # After 2 trading days, exit if we're green
            if now >= entry_time + timedelta(days=2):
                if current_price > entry_price:
                    proceeds = broker.sell(symbol, shares, current_price)
                    print(f"📆 Exiting after 2 days @ ${current_price:.2f} (green). Proceeds: ${proceeds:,.2f}")
                    break
                else:
                    print(f"⌛ Day 2+... Still watching. Current: ${current_price:.2f}, Entry: ${entry_price:.2f}")

            time.sleep(60)

        print(f"🏁 Updated balance: ${broker.get_balance():,.2f}")
        print("🔄 Looking for next IPO...\n")


if __name__ == "__main__":
    run_bot()
