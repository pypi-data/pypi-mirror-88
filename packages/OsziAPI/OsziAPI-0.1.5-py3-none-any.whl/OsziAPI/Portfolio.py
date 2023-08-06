import pandas as pd

from OsziAPI.Currency import Currency
from OsziAPI.Fund import Fund


class Portfolio:
    def __init__(self,
                 list_of_fund_id=None,
                 list_of_fund_hpid=None,
                 currency='USD'):
        if list_of_fund_id:
            self.funds = [Fund(fund_id=fund_id) for fund_id in list_of_fund_id]
        else:
            self.funds = [Fund(hpid=hpid) for hpid in list_of_fund_hpid]
        self.currency = Currency(currency_code=currency)

    def get_list_of_returns(self):
        for fund in self.funds:
            fund.get_leading_series()
        self.convert_return_in_portfolio_currency()
        try:
            return pd.concat([fund.returns_in_portfolio_currency.rename
                              (columns={"value": fund.name})
                              for fund in self.funds], axis=1)
        except ValueError:
            return None

    def convert_return_in_portfolio_currency(self):
        portfolio_libor = self.currency.libor.load_ticker_values('PX_LAST')
        for fund in self.funds:
            fund.calculate_returns_in_portfolio_currency(portfolio_libor)
