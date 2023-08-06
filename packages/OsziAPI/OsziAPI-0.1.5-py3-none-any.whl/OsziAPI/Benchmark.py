from decimal import Decimal

import numpy as np
import pandas as pd

from OsziAPI import DatabaseAPI
from OsziAPI.DatabaseAPI import get_db_data
from OsziAPI.Ticker import Ticker


class Benchmark:
    def __init__(self, benchmark_id):
        self.id = benchmark_id
        self.name = get_db_data(self.id, 'benchmark', 'benmark_name')

    def __str__(self):
        print(self.name)

    @property
    def benchmark_value(self):
        return DatabaseAPI.get_benchmark_composition(self.id)

    @property
    def benchmark_returns(self):
        composition = self.benchmark_value
        tickers = set(composition.ticker_id.to_list())
        list_df = []
        ticker_df = []
        for ticker in tickers:
            df = composition[composition.ticker_id == ticker]
            df = df.set_index('value_date')
            df.drop(['id', 'benchmark_id', 'ticker_id'], inplace=True, axis=1)
            df.rename(columns={'percent': ticker}, inplace=True)
            list_df.append(df)
            ticker_values = Ticker(ticker).load_ticker_values()
            ticker_values.rename(columns={'value': ticker}, inplace=True)
            ticker_df.append(ticker_values)
        weights_df = pd.concat(list_df, axis=1)
        weights_df.fillna(Decimal(np.NaN), inplace=True)
        weights_df = weights_df.div(np.nansum(weights_df, axis=1), axis=0)
        tickers = pd.concat(ticker_df, axis=1)
        tickers = tickers.loc[weights_df.index[0]:]
        weights_df = weights_df.reindex(tickers.index, method='ffill')
        for ticker in tickers:
            weights_df[ticker] = weights_df[ticker].mul(tickers[ticker])
        weights_df['benchmark'] = np.nansum(weights_df, axis=1)
        weights_df[self.name] = weights_df['benchmark'].astype(
            'float').pct_change()
        return weights_df[[self.name]]

    def ytd_returns(self, report_date=None):
        returns = self.benchmark_returns[:report_date]
        report_date = returns.index[-1]
        return (returns[str(report_date.year):report_date] + 1).cumprod().iloc[
                   -1].values[0] - 1

    def annualized_returns(self, start_date=None, report_date=None):
        """
        returns annualized returns over the given period
        :param start_date:
        :param report_date:
        :return: float
        """
        if start_date is None:
            start_date = self.benchmark_returns.index[0]
        if report_date is None:
            report_date = self.benchmark_returns.index[-1]
        returns = self.benchmark_returns[start_date:report_date]
        return float((returns + 1).cumprod().tail(1).values[0][0]) \
            ** (12 / len(returns)) - 1

    def annualized_vol(self, start_date=None, report_date=None):
        if start_date is None:
            start_date = self.benchmark_returns.index[0]
        if report_date is None:
            report_date = self.benchmark_returns.index[-1]
        returns = self.benchmark_returns[start_date:report_date]
        return returns.astype('float').std()[0] * 12 ** 0.5

    def sharpe_ratio(self):
        pass


if __name__ == '__main__':
    bm = Benchmark(4)
    print(bm.benchmark_returns)
