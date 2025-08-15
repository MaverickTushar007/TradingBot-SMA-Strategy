# SMA Trading Bot

A simple Python trading bot that uses a **Simple Moving Average (SMA)** strategy to generate Buy, Sell, or Hold signals and simulate trades with a mock trading API.

---

## Features

- Base trading bot class for extensibility.
- SMA strategy with customizable short and long windows.
- Trade object tracks signal, amount, ticker, and timestamp.
- Mock trading API to simulate trades and account balance.
- Trading system fetches historical prices from Yahoo Finance.
- Logs include ticker symbols for clarity.

---

## Usage

```python
symbol = "JPM"
api = MockTradingAPI(balance=100000)
strategy = MySMATradingStrategy("SMA Strategy", swindow=3, lwindow=10)
system = MyTradingSystem(api, strategy, symbol)

for i in range(2):
    system.run()
    print(f"Remaining balance: {api.balance}")
