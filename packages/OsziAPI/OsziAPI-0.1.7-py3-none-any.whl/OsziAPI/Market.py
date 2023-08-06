import pandas as pd

from OsziAPI import DatabaseAPI
from OsziAPI.Ticker import Ticker
from OsziAPI.Fund import Fund


class MarketData:
    def __init__(self):
        self.tickers = [Ticker(item[0]) for item in
                        DatabaseAPI.get_all_tickers()]
        self.tickers = [ticker for ticker in self.tickers
                        if ticker.ticker_name is None
                        or (ticker.ticker_name and ("Month" not in
                                                    ticker.ticker_name))]

    def get_market_returns(self):
        market_returns = pd.concat([ticker.load_ticker_values() for ticker in
                                    self.tickers], axis=1).astype(
            'float').pct_change()
        market_returns.columns = [ticker.bbg_ticker for ticker in self.tickers]
        return market_returns

    def filter_funds(self, list_funds):
        self.tickers = [ticker for ticker in self.tickers
                        if (ticker.ticker_name and (ticker.bbg_ticker in
                                                    list_funds))]


class AllFunds:
    def __init__(self):
        self.funds = [Fund(item[0]) for item in
                      DatabaseAPI.get_all_funds()]

    def leading_series(self):
        all_leading_series = pd.concat([fund.leading_series for fund in
                                        self.funds], axis=1)
        all_leading_series.columns = [fund.id for fund in self.funds]
        return all_leading_series


if __name__ == '__main__':
    all_series = AllFunds().leading_series()
