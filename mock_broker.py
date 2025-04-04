# mock_broker.py

import random

class MockBroker:
    def __init__(self, starting_balance=100000):
        self.balance = starting_balance
        self.positions = {}  # {symbol: (shares, avg_price)}

    def get_balance(self):
        return self.balance

    def get_price(self, symbol):
        """Simulate price movement for a symbol."""
        if symbol in self.positions:
            # Simulate price after entry
            entry_price = self.positions[symbol][1]
            return round(entry_price * random.uniform(0.97, 1.13), 2)
        else:
            # Pre-entry IPO market price simulation
            return round(random.uniform(5.0, 15.0), 2)

    def buy(self, symbol, shares, price):
        cost = shares * price
        if self.balance < cost:
            raise ValueError("Insufficient funds")

        self.balance -= cost
        self.positions[symbol] = (shares, price)
        return price  # Simulated avg fill

    def sell(self, symbol, shares, price):
        if symbol not in self.positions:
            raise ValueError("No shares to sell")

        held_shares, entry_price = self.positions[symbol]
        if shares > held_shares:
            raise ValueError("Not enough shares to sell")

        proceeds = shares * price
        self.balance += proceeds
        del self.positions[symbol]
        return proceeds
