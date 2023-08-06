import datetime as dt
from datetime import date
from decimal import Decimal

import numpy as np
import pandas as pd

from OsziAPI import DatabaseAPI
from OsziAPI.DatabaseAPI import get_db_data
from OsziAPI.Security import Security


class Position:
    def __init__(self, position_id):
        self.id = position_id
        self.table_name = 'positions'
        self.end_month_mv = None
        self.end_month_mv_base_for_cont = None
        self.end_market_value_base_adj_for_contribution = None
        self.end_market_value_local = None
        self.end_market_value_local_for_cont = None
        self.end_market_value_local_adj_for_contribution = None
        self.market_value_t_minus1_calc = None
        self.hist_adj_ytd_cont_product = None
        self.allocation_portfolio_T_minus_1 = None
        self.allocation_product_T_minus_1 = None
        self.mtd_contribution_product = None
        self.adj_mtd_contribution_product = None
        self.adj_ytd_contribution_product = None
        self.end_month_mv_date = None

    @property
    def fund_id(self):
        return get_db_data(self.id, self.table_name, 'fund_id')

    @property
    def lookthrough(self):
        return get_db_data(self.id, self.table_name, 'lookthrough')

    def is_current(self, report_date):
        # only not current if ror is none
        date_list = pd.date_range(dt.date(report_date.year, 1, 31),
                                  report_date, freq='1M').to_list()
        return \
            any(~np.isnan(
                [float(self.get_end_marktet_value_base(day.to_pydatetime(
                ))) for day in date_list] +
                [float(self.get_end_marktet_value_base(report_date))]))

    def get_end_price_date(self, report_date):
        end_mv_date = self.get_end_mv_date(report_date)
        end_ror_date = self.security.get_end_mtd_ror(report_date).value_date
        if end_mv_date and end_ror_date:
            return max([end_mv_date, end_ror_date])
        elif end_mv_date or end_ror_date:
            return end_mv_date or end_ror_date
        else:
            return None

    @property
    def active(self):
        return get_db_data(self.id, self.table_name, 'active_passive')

    @property
    def position_type(self):
        return get_db_data(self.id, self.table_name, 'position_type')

    @property
    def series_id(self):
        return get_db_data(self.id, self.table_name, 'series_id')

    @property
    def fund(self):
        from OsziAPI.Fund import Fund
        return Fund(self.fund_id)

    @property
    def security(self):
        return Security(self.series_id)

    @property
    def position_shares(self):
        return DatabaseAPI.get_position_shares(self.id)

    def get_weights(self, date_list):
        position_shares = self.position_shares[
            self.position_shares.report_date.isin(date_list)]
        position_shares = \
            position_shares[position_shares.share.notnull()]
        position_shares.sort_values(
            ['end_shares_date', 'data_entry_date'],
            ascending=[False, False], inplace=True)
        position_shares = position_shares.groupby('report_date').first()
        return position_shares[['share']]

    def get_weights_t_minus_one(self, date_list):
        weights_minus_one = \
            DatabaseAPI.get_position_history(self.id, 'mv_T_minus_1_calc')
        weights_minus_one = weights_minus_one[
            weights_minus_one.report_date.isin(date_list)].copy()
        weights_minus_one.sort_values(
            ['report_date', 'value_date', 'data_entry_date', 'final'],
            ascending=[True, False, False, False], inplace=True)
        weights_minus_one = weights_minus_one.groupby('report_date').first()
        return weights_minus_one[['value']]

    def category(self, report_date):
        from OsziAPI.Fund import Fund
        fund = Fund(self.security.passive_positions[0].fund_id,
                    get_positions=False)
        if self.get_end_marktet_value_base(report_date).is_nan() \
                or (not self.end_month_mv
                    and not self.get_mtd_cont_product(report_date)):
            _category = '6-Redeemed'
        elif self.security.investment_status == 'side_pocket':
            _category = '4-Side Pocket'
        elif fund.type == 'closed_end_fund':
            _category = '3-COF'
        elif fund.redemption_freq in ['weekly', 'Weekly', 'daily', 'Daily'] and \
                not fund.not_liquid_alternative:
            _category = '2-Liquid Alts'
        elif fund.style == 'relative_value':
            _category = '1a-MS/RV'
        elif fund.bucket == 'divergence':
            _category = '1b-Divergence'
        elif fund.style == 'event_driven':
            _category = '1c-MS/ED'
        else:
            _category = '5-Cash + RNA'
        return _category

    def get_end_marktet_value_base(self, report_date=date.today(), final=0):
        """
        Returns the end market value given the report date
        :param report_date:
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.end_month_mv = \
            DatabaseAPI.get_end_mv_base(self.id, report_date, final)
        return self.end_month_mv

    def get_end_mv_date(self, report_date=date.today(), final=0):
        """
        Returns the end market value given the report date
        :param report_date:
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.end_month_mv_date = \
            DatabaseAPI.get_end_mv_date(self.id, report_date, final)
        return self.end_month_mv_date

    def get_market_value_t_minus1_calc(self, report_date=date.today(), final=0):
        """
        Returns the end market value of t-1 given the report date
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.market_value_t_minus1_calc = \
            self.get_position_history('mv_T_minus_1_calc', report_date,
                                      final)
        return self.market_value_t_minus1_calc

    def get_mtd_cont_product(self, report_date, final=0):
        """
        Get month to date contribution product
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.mtd_contribution_product = \
            self.get_position_history('mtd_cont_product', report_date,
                                      final)
        return self.mtd_contribution_product

    def get_adj_mtd_cont_product(self, report_date, final=0):
        """
        Get adjusted month to date contribution product
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.adj_mtd_contribution_product = \
            self.get_position_history('adj_mtd_cont_product', report_date,
                                      final)
        return self.adj_mtd_contribution_product

    def get_adj_ytd_cont_product(self, report_date, final=0):
        """
        Get adjusted year to date contribution product
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.adj_ytd_contribution_product = \
            self.get_position_history('adj_ytd_cont_prod', report_date,
                                      final)
        return self.adj_ytd_contribution_product

    def get_end_market_value_local(self, report_date=date.today(), final=0):
        self.end_market_value_local = \
            DatabaseAPI.get_end_mv_local(self.id,
                                         report_date,
                                         final)[0]
        return self.end_market_value_local

    def get_end_market_value_local_for_cont(self, report_date=date.today(),
                                            final=0):
        self.end_market_value_local_for_cont = \
            DatabaseAPI.get_end_mv_local_for_cont(self.id,
                                                  report_date,
                                                  final)[0]
        return self.end_market_value_local_for_cont

    def get_end_market_value_local_adj_for_cont(self, report_date=date.today(),
                                                final=0):
        self.end_market_value_local_adj_for_contribution = \
            DatabaseAPI.get_end_mv_local_adj_for_cont(self.id,
                                                      report_date,
                                                      final)[0]
        return self.end_market_value_local_adj_for_contribution

    def get_fx(self):
        fx = DatabaseAPI.get_position_history(self.id, 'fx')
        return fx
    fx = property(get_fx)

    def get_allocation_portfolio_t_minus1(self, report_date, final=0):
        self.allocation_portfolio_T_minus_1 = \
            self.get_position_history('allocation_portfolio_T_minus_1',
                                      report_date,
                                      final)
        return self.allocation_portfolio_T_minus_1

    def get_allocation_product_t_minus1(self, report_date, final=0):
        self.allocation_product_T_minus_1 = \
            self.get_position_history('allocation_product_T_minus_1',
                                      report_date,
                                      final)
        return self.allocation_product_T_minus_1

    def get_end_market_value_base_for_cont(self, report_date=date.today(),
                                           final=0):
        """
        Returns the end market value base for contribution given the report date
        :param report_date: datetime date
        :param final: 0 by default if estimates can be considered. 1 for
        final data only
        :return:
        """
        self.end_month_mv_base_for_cont = \
            DatabaseAPI.get_end_mv_base_for_cont(
                self.id, report_date, final)[0]
        return self.end_month_mv_base_for_cont

    def get_hist_adj_ytd_cont_product(self, report_date=date.today(),
                                      final=0):
        self.hist_adj_ytd_cont_product = \
            self.get_position_history('hist_adj_ytd_cont_product',
                                      report_date,
                                      final)
        return self.hist_adj_ytd_cont_product

    def get_position_history(self, data_field, report_date, final):
        position_history = \
            DatabaseAPI.get_position_history_value(
                self.id, data_field, report_date, final)
        if position_history is None:
            return Decimal(np.NAN)
        return position_history[0]

    def get_end_market_value_base_adj_for_cont(self, report_date=date.today(),
                                               final=0):
        self.end_market_value_base_adj_for_contribution = \
            DatabaseAPI.get_end_mv_base_adj_for_cont(
                self.id, report_date, final)[0]
        return self.end_market_value_base_adj_for_contribution

    def get_beg_market_value_local(self):
        beg_market_value_local = DatabaseAPI.get_position_history(
            self.id, 'beg_mv_local')
        return beg_market_value_local
    beg_market_value_local = property(get_beg_market_value_local)

    def get_beg_market_value_base(self):
        beg_market_value_base = \
            DatabaseAPI.get_position_history(self.id, 'beg_mv_base')
        return beg_market_value_base
    beg_market_value_base = property(get_beg_market_value_base)

    def get_total_commitment(self):
        total_commitment = \
            DatabaseAPI.get_position_history(self.id, 'total_commitment')
        return total_commitment
    total_commitment = property(get_total_commitment)

    def get_funded_commitment(self):
        funded_commitment = \
            DatabaseAPI.get_position_history(self.id, 'funded_commitment')
        return funded_commitment
    funded_commitment = property(get_funded_commitment)

    def get_unfunded_commitment(self):
        unfunded_commitment = \
            DatabaseAPI.get_position_history(self.id, 'unfunded_commitment')
        return unfunded_commitment
    unfunded_commitment = property(get_unfunded_commitment)

    def get_total_distributions_to_date(self):
        total_distribution_to_date = \
            DatabaseAPI.get_position_history(self.id,
                                             'total_distributions_to_date')
        return total_distribution_to_date
    total_distribution_to_date = property(get_total_distributions_to_date)

    def get_picc(self):
        picc = DatabaseAPI.get_position_history(self.id, 'picc')
        return picc
    picc = property(get_picc)

    def get_dpi(self):
        dpi = DatabaseAPI.get_position_history(self.id, 'dpi')
        return dpi
    dpi = property(get_dpi)


if __name__ == '__main__':
    position = Position(1014)
    position.monthly_report_output(date(2020, 7, 31))
    print("test")
