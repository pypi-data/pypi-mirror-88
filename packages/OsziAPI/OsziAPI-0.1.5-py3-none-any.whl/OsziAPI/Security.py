import datetime

import pandas as pd

from OsziAPI import Helper, DatabaseAPI
from OsziAPI.Currency import Currency
from OsziAPI.DatabaseAPI import get_db_data
from OsziAPI.Returns import RateOfReturn


class Security:
    def __init__(self, sec_id):
        self.id = sec_id
        self.table_name = 'securities'
        self.mtd_returns = None
        self.current_mtd_ror = None
        self.end_1y_ror = None
        self.allocation_portfolio_T_minus_1 = None
        self.allocation_product_T_minus_1 = None
        self.hist_ror_ytd = None
        self.beg_mtd_ror = None
        self.beg_ytd_ror = None
        self.beg_y_ror = None
        self.end_mtd_ror = None
        self.end_ytd_ror = None
        self.mtd_contribution_portfolio = None
        self.adj_mtd_contribution_portfolio = None
        self.adj_ytd_contribution_portfolio = None
        self.hist_adj_ytd_contribution_portfolio = None

    def __str__(self):
        return self.series_name

    @property
    def active_positions(self):
        """
                Get list of the active positions with the security id
                :return:
                """
        from OsziAPI.Position import Position
        active_position_ids = DatabaseAPI.get_position_id_by_security_id(
            self.id, 1)
        if active_position_ids:
            _active_positions = [Position(position_id) for
                                 position_id
                                 in active_position_ids]
        else:
            return None
        return _active_positions

    @property
    def passive_positions(self):
        """
        Get list of the passive positions with the security id
        :return:
        """
        from OsziAPI.Position import Position
        passive_position_ids = DatabaseAPI.get_position_id_by_security_id(
            self.id, 0)
        if passive_position_ids:
            _passive_positions = [Position(position_id) for
                                  position_id
                                  in passive_position_ids]
        else:
            return None
        return _passive_positions

    @property
    def fund(self):
        """
        Get list of the passive positions with the security id
        :return:
        """
        from OsziAPI.Position import Position
        passive_position_ids = DatabaseAPI.get_position_id_by_security_id(
            self.id, 0)
        if passive_position_ids:
            _passive_positions = [Position(position_id) for
                                  position_id
                                  in passive_position_ids]
        else:
            return None
        return _passive_positions[0].fund

    @property
    def share_class(self):
        """
        Get the share class
        :return:
        """
        return get_db_data(self.id, self.table_name, 'share_class')

    @property
    def isin(self):
        """
        Get the ISIN of the security
        :return:
        """
        return get_db_data(self.id, self.table_name, 'ISIN')

    @property
    def series_name(self):
        """
        Get the series name
        :return:
        """
        return get_db_data(self.id, self.table_name, 'series_name')

    @property
    def hpid(self):
        """
        Get the hpid of the security
        :return:
        """
        return get_db_data(self.id, self.table_name, 'hpid')

    @property
    def currency(self):
        """
        Get the currency of the security
        :return:
        """
        currency_id = get_db_data(self.id, self.table_name, 'currency_id')
        if currency_id:
            _currency = Currency(currency_id)
        else:
            _currency = security.fund.currency
        return _currency

    @property
    def investment_status(self):
        return get_db_data(self.id, self.table_name, 'investment_status')

    @property
    def dealing_comments_securities(self):
        """
        Get the dealing comments of the security
        :return:
        """
        return get_db_data(self.id, self.table_name,
                           'dealing_comments_securities')

    @property
    def management_fee_percent(self):
        """
        Get the
        :return:
        """
        return get_db_data(self.id, self.table_name, 'management_fee_percent')

    @property
    def management_fee_freq(self):
        return get_db_data(self.id, self.table_name, 'management_fee_percent')

    @property
    def performance_fee_percent(self):
        return get_db_data(self.id, self.table_name, 'performance_fee_percent')

    @property
    def performance_fee_freq(self):
        return get_db_data(self.id, self.table_name, 'performance_fee_freq')

    @property
    def fees_comments(self):
        return get_db_data(self.id, self.table_name, 'fees_comments')

    @property
    def issues_equalisation(self):
        return get_db_data(self.id, self.table_name, 'issues_equalisation')

    @property
    def high_water_mark(self):
        return get_db_data(self.id, self.table_name, 'high_water_mark')

    @property
    def hurdle_rate(self):
        return get_db_data(self.id, self.table_name, 'hurdle_rate')

    @property
    def share_class_specific_terms(self):
        return get_db_data(self.id, self.table_name,
                           'share_class_specific_terms')

    @property
    def all_returns(self):
        """
        Get all entries from the table "returns" of the security
        :return:
        """
        return DatabaseAPI.get_returns(self.id)

    def get_mtd_returns(self, date_list=pd.date_range(datetime.date(1900, 1,
                                                                    1),
                                                      datetime.date(2100, 1,
                                                                    1),
                                                      freq='M'),
                        final=0):
        """
        Get the end of month returns with the date_list of the security
        :param date_list:
        :param final:
        :return:
        """
        df_end_mtd_returns = DatabaseAPI.get_end_mtd_returns(self.id)
        df_end_mtd_returns = \
            df_end_mtd_returns[df_end_mtd_returns['value_date']
                               >= df_end_mtd_returns['report_date'].apply(
                lambda dt: dt.replace(day=1))]
        mtd_returns = \
            df_end_mtd_returns[
                (df_end_mtd_returns['report_date'].isin(date_list)) &
                (df_end_mtd_returns['final'] >= final)].copy()
        mtd_returns.sort_values(
            ['value_date', 'final', 'data_entry_date'],
            ascending=[False, False, False], inplace=True)
        self.mtd_returns = mtd_returns.groupby('report_date').first()
        return self.mtd_returns[['value']] / 100

    @property
    def end_prices(self, final=0):
        """
        Get end prices as DataFrame
        :param final:
        :return:
        """
        return DatabaseAPI.get_end_price(self.id, final)

    def get_current_mtd_ror(self, report_date, final=0):
        """
        Get the end mtd ror for report date
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.current_mtd_ror = \
            RateOfReturn(*self.get_return(report_date,
                                          'current_month_mtd_ror',
                                          final))
        return self.current_mtd_ror

    def get_end_mtd_ror(self, report_date, final=0):
        """
        Get the end mtd ror for report date
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.end_mtd_ror = \
            RateOfReturn(*DatabaseAPI.get_end_mtd_ror(self.id,
                                                      report_date,
                                                      final))
        return self.end_mtd_ror

    def get_ytd_ror_from_mtd_ror(self, report_date, final=0):
        """
        Calculate the ytd_ror from the mtd ror
        :param report_date:
        :param final:
        :return:
        """
        date_list = pd.date_range(datetime.date(report_date.year, 1, 31),
                                  report_date, freq='1M').to_list()
        if report_date not in date_list:
            date_list.append(report_date)
        df = self.get_mtd_returns(date_list, final)
        if df.empty:
            return RateOfReturn(None, None, None)
        ytd_ror = ((df.value + 1).cumprod() - 1)[-1]
        return RateOfReturn(ytd_ror, df.index[-1], final)

    def get_end_ytd_ror(self, report_date, final=0):
        """
        Get the end ytd ror for report date
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.end_ytd_ror = \
            RateOfReturn(*DatabaseAPI.get_end_ytd_ror(self.id,
                                                      report_date,
                                                      final))
        return self.end_ytd_ror

    def get_end_1y_ror(self, report_date, final=0):
        self.end_1y_ror = \
            RateOfReturn(*DatabaseAPI.get_end_y_ror(self.id,
                                                    report_date,
                                                    final))
        return self.end_1y_ror

    def get_allocation_product_t_minus1(self, report_date, final=0):
        self.allocation_product_T_minus_1 = \
            RateOfReturn(*self.get_return(report_date,
                                          'allocation_product_T_minus_1',
                                          final))
        return self.allocation_product_T_minus_1

    def get_mtd_cont_portfolio(self, report_date, final=0):
        self.mtd_contribution_portfolio = \
            RateOfReturn(*self.get_return(report_date,
                                          'mtd_cont_portfolio',
                                          final))
        return self.mtd_contribution_portfolio

    def get_adj_mtd_cont_portfolio(self, report_date, final=0):
        self.adj_mtd_contribution_portfolio = \
            RateOfReturn(*self.get_return(report_date,
                                          'adj_mtd_cont_portfolio',
                                          final))
        return self.adj_mtd_contribution_portfolio

    def get_return(self, report_date, return_type, final=0):
        df = \
            self.all_returns[
                (self.all_returns['value_date']
                 >= pd.to_datetime(report_date).replace(day=1)) &
                (self.all_returns['final'] >= final) &
                (self.all_returns['report_date']
                 == pd.to_datetime(report_date)) &
                (self.all_returns['return_type']
                 == return_type)].copy()
        df.sort_values(
            ['value_date', 'data_entry_date', 'final'],
            ascending=[False, False, False], inplace=True)
        if len(df) == 0:
            return None, None, None
        return df.iloc[0]['value'], df.iloc[0]['value_date'], df.iloc[0][
            'final']

    def get_adj_ytd_cont_portfolio(self, report_date, final=0):
        self.adj_ytd_contribution_portfolio = \
            RateOfReturn(*self.get_return(report_date,
                                          'adj_ytd_cont_portf',
                                          final))
        return self.adj_ytd_contribution_portfolio

    def get_hist_ror_ytd(self, report_date, final=0):
        """
        Get historical ror year to date
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.hist_ror_ytd = \
            RateOfReturn(*self.get_return(report_date,
                                          'hist_ror_ytd',
                                          final))
        return self.hist_ror_ytd

    def get_hist_adj_ytd_cont_portfolio(self, report_date, final=0):
        self.hist_adj_ytd_contribution_portfolio = \
            RateOfReturn(*self.get_return(report_date,
                                          'hist_adj_ytd_cont_portfolio',
                                          final))
        return self.hist_adj_ytd_contribution_portfolio

    def get_beg_mtd_ror(self, report_date, final=0):
        self.beg_mtd_ror = \
            RateOfReturn(*self.get_return(report_date, 'beg_mtd_ror', final))
        return self.beg_mtd_ror

    def get_beg_ytd_ror(self, report_date, final=0):
        self.beg_ytd_ror = \
            RateOfReturn(*self.get_return(report_date, 'beg_ytd_ror', final))
        return self.beg_ytd_ror

    def get_beg_1y_ror(self, report_date, final=0):
        self.beg_y_ror = \
            RateOfReturn(*self.get_return(report_date, 'beg_y_ror', final))
        return self.beg_y_ror

    @property
    def risk_free_rate(self):
        return self.currency.libor.load_ticker_values()

    @property
    def excess_return(self):
        """
        returns excess return over the currency risk free rate
        :return:
        """
        return (self.get_mtd_returns() - self.risk_free_rate).dropna()

    def ytd_returns(self, report_date=None):
        """
        returns year to date returns
        :param report_date:
        :return:
        """
        returns = self.get_mtd_returns()[:report_date]
        report_date = returns.index[-1]
        return float((returns[str(report_date.year):report_date] +
                1).cumprod().iloc[-1].values[0] - 1)

    def benchmark_ytd_returns(self, report_date=None):
        return self.fund.benchmark_reporting.ytd_returns(report_date)

    def annualized_returns(self, start_date=None, report_date=None):
        """
        returns annualized returns over the given period
        :param start_date:
        :param report_date:
        :return: float
        """
        if start_date is None:
            start_date = self.get_mtd_returns().index[0]
        if report_date is None:
            report_date = self.get_mtd_returns().index[-1]
        returns = self.get_mtd_returns()[start_date:report_date]
        return float((returns + 1).cumprod().tail(1).values[0][0]) \
            ** (12 / len(returns)) - 1

    def annualized_vol(self, start_date=None, report_date=None):
        """
        returns annualized volatility
        :param start_date:
        :param report_date:
        :return:
        """
        if start_date is None:
            start_date = self.get_mtd_returns().index[0]
        if report_date is None:
            report_date = self.get_mtd_returns().index[-1]
        returns = self.get_mtd_returns()[start_date:report_date]
        return returns.astype('float').std()[0] * 12 ** 0.5

    def benchmark_annualized_returns(self, start_date=None, report_date=None):
        return self.fund.benchmark_reporting.annualized_returns(start_date,
                                                                report_date)

    def benchmark_annualized_vol(self, start_date=None, report_date=None):
        return self.fund.benchmark_reporting.annualized_returns(
            start_date, report_date)

    def sharpe_ratio(self):
        pass


if __name__ == '__main__':
    security = Security(1006)
    print(security.risk_free_rate)
    print(security.excess_return)
    print(security.ytd_returns())
    print(security.benchmark_ytd_returns())
    print(security.annualized_returns())
    print(security.annualized_vol())
    print(security.benchmark_annualized_vol())
    print(security.benchmark_annualized_returns())

    security.get_mtd_returns(
        date_list=Helper.months_in_range(datetime.date(2000, 1, 1),
                                         datetime.date(2020, 7, 31)),
        final=1)
    print("test accomplished")
