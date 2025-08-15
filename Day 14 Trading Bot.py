from datetime import datetime
import yfinance as yf
import time

# ------------------ Base Trading Bot ------------------
class MyTradingBot:
    def __init__(self, name):
        self.__name = name

    def generate(self, price_data):
        print("This method should be overridden in subclasses")
        return "Hold"

    @property
    def name(self):
        return self.__name

# ------------------ SMA Strategy ------------------
class MySMATradingStrategy(MyTradingBot):
    def __init__(self, name, swindow, lwindow):
        super().__init__(name)
        self.__swindow = swindow
        self.__lwindow = lwindow

    def generate(self, price_data):
        if len(price_data) < self.__lwindow:
            return "Hold"

        short_avg = sum(price_data[-self.__swindow:]) / self.__swindow
        long_avg = sum(price_data[-self.__lwindow:]) / self.__lwindow

        if short_avg > long_avg:
            return "Buy"
        elif long_avg > short_avg:
            return "Sell"
        else:
            return "Hold"

    @property
    def swindow(self):
        return self.__swindow

    @property
    def lwindow(self):
        return self.__lwindow

# ------------------ Trade Object ------------------
class MyTrade:
    def __init__(self, str_name, signal, amount, symbol):
        self.__str_name = str_name
        self.__signal = signal
        self.__amount = amount
        self.__symbol = symbol
        self.__timestamp = datetime.now()

    def execute(self):
        print(f"Trade for '{self.__symbol}' has been executed {self.__signal} trade with strategy {self.__str_name} "
              f"for amount {self.__amount} at {self.__timestamp}")

    @property
    def str_name(self):
        return self.__str_name

    @property
    def symbol(self):
        return self.__symbol

    @property
    def signal(self):
        return self.__signal

    @property
    def amount(self):
        return self.__amount

    @property
    def timestamp(self):
        return self.__timestamp

# ------------------ Mock Trading API ------------------
class MockTradingAPI:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def placeOrder(self, trade, price):
        if trade.signal == "Buy" and self.__balance >= trade.amount * price:
            self.__balance -= trade.amount * price
            print(f'Placed BUY trade at {price}, remaining balance: {self.__balance}')
        elif trade.signal == "Sell":
            self.__balance += trade.amount * price
            print(f'Placed SELL trade at {price}, new balance: {self.__balance}')
        else:
            print("Insufficient balance or invalid signal")

# ------------------ Trading System ------------------
class MyTradingSystem:
    def __init__(self, api, strategy, symbol):
        self.__api = api
        self.__strategy = strategy
        self.__symbol = symbol
        self.__price_data = []

    def fetch_price_data(self):
        # Download historical prices as a Series
        data = yf.download(tickers=self.__symbol, period="6mo", interval="1d")['Close'].squeeze()
        if not data.empty:
            # Keep only the last 'lwindow' prices for SMA calculation
            self.__price_data = data[-self.__strategy.lwindow:].tolist()

            # Current price is the last value in data
            price = self.__price_data[-1]

            print(f'Price updated: {price}, current balance: {self.__api.balance}')
        else:
            print("No data fetched!")

    def run(self):
        self.fetch_price_data()
        signal = self.__strategy.generate(self.__price_data)
        print(f"Generated signal: {signal}")

        if signal in ["Buy", "Sell"]:
            trade = MyTrade(self.__strategy.name, signal, 1, self.__symbol)
            trade.execute()
            self.__api.placeOrder(trade, self.__price_data[-1])

    @property
    def api(self):
        return self.__api

    @property
    def strategy(self):
        return self.__strategy

    @property
    def symbol(self):
        return self.__symbol

# ------------------ Testing ------------------
# Test SMA Strategy
signal_strategy = MySMATradingStrategy("SMA Strategy", swindow=9, lwindow=21)
sample_prices = [4, 2, 1, 45, 62, 1, 1, 1]
print(f"Test SMA Signal: {signal_strategy.generate(sample_prices)}\n")

# Test Trade and Mock API
symbol = "JPM"
test_trade = MyTrade("SMA", "Buy", 100, symbol)
mock_api = MockTradingAPI(10000)
mock_api.placeOrder(test_trade, 200)

# Test Trading System
api = MockTradingAPI(balance=100000)
strategy = MySMATradingStrategy("SMA Strategy", swindow=3, lwindow=7)
system = MyTradingSystem(api, strategy, symbol)

for i in range(2):
    print(f"\n--- Run {i + 1} ---")
    system.run()
    print(f"Remaining balance: {api.balance}")
    time.sleep(2)


