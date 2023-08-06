from datetime import date

from OsziAPI import Helper, DatabaseAPI
from OsziAPI.Agent import Agent
from OsziAPI.Country import Country
from OsziAPI.Currency import Currency
from OsziAPI.DatabaseAPI import get_db_data, get_fund_attribute_by_date, \
    get_fund_attribute_value_by_date
from OsziAPI.Position import Position
from OsziAPI.Benchmark import Benchmark


class Fund:
    def __init__(self, fund_id=None, hpid=None, get_positions=True):
        self.table_name = 'funds'
        if fund_id:
            self.id = fund_id
        else:
            self.id = DatabaseAPI.get_fund_id_by_hpid(hpid)
        self.hpid = None
        self.get_hpid_by_id()
        self.attribute_table = 'fund_attribute'
        self.actives = None
        self.passives = None
        if get_positions:
            self.get_active_positions()
            self.get_passive_positions()
        self.fund_info = self.get_fund_static_data()
        self.benchmark_powerBI = None
        self.target_return = None
        self.returns_in_portfolio_currency = None
        self.current_active_positions = None

    @property
    def benchmark_reporting_id(self):
        return self.fund_info['benchmark_reporting'][0]

    @property
    def reporting_benchmark_returns(self):
        return Benchmark(self.benchmark_reporting_id).benchmark_returns

    def get_portfolio_ytd(self, report_date=date.today()):
        return DatabaseAPI.get_fund_history(self.id, 'portfolio_ytd',
                                            report_date)

    def get_product_ytd(self, report_date=date.today()):
        return DatabaseAPI.get_fund_history(self.id, 'product_ytd',
                                            report_date)

    def get_current_active_positions(self, report_date, lookthrough=0):
        self.current_active_positions \
            = [position for position in self.actives
               if position.is_current(report_date) and
               lookthrough == position.lookthrough]
        return self.current_active_positions

    @property
    def name(self):
        return self.fund_info['fund_name'][0]

    @property
    def short_name(self):
        if self.fund_info['fund_name_short'][0] is not None:
            return self.fund_info['fund_name_short'][0]
        return self.fund_info['fund_name'][0]

    def __str__(self):
        return self.name

    def get_fund_static_data(self):
        self.fund_info = DatabaseAPI.get_fund_info(self.id)
        return self.fund_info

    def get_positions(self):
        self.actives = self.get_active_positions()
        self.passives = self.get_passive_positions()

    def get_hpid_by_id(self):
        if self.id:
            self.hpid = get_db_data(self.id, self.table_name, 'hpid')
        else:
            self.id = DatabaseAPI.get_fund_id_by_hpid(self.hpid)

    def get_hp_strategy(self, report_date=date.today()):
        hp_strategy = get_fund_attribute_by_date(self.id,
                                                 'hp_strategy',
                                                 report_date)
        return hp_strategy

    hp_strategy = property(get_hp_strategy)

    def check_liquid_alternative(self, report_date=date.today()):
        not_la = get_fund_attribute_value_by_date(self.id,
                                                  'not_liquid_alternative',
                                                  report_date)
        return not_la

    not_liquid_alternative = property(check_liquid_alternative)

    def get_hp_substrategy(self, report_date=date.today()):
        hp_sub_strategy = get_fund_attribute_by_date(self.id,
                                                     'hp_substrategy',
                                                     report_date)
        return hp_sub_strategy

    hp_sub_strategy = property(get_hp_substrategy)

    def get_redemption_freq(self, report_date=date.today()):
        redemption_freq = get_fund_attribute_by_date(self.id,
                                                     'redemption_freq',
                                                     report_date)
        return redemption_freq

    redemption_freq = property(get_redemption_freq)

    def get_fund_type(self):
        fund_type = self.fund_info['type'][0]
        return fund_type
    type = property(get_fund_type)

    def get_fund_country(self):
        country_id = self.fund_info['domicile'][0]
        country = Country(country_id)
        return country
    country = property(get_fund_country)

    def get_fund_currency(self):
        currency_id = self.fund_info['currency_id'][0]
        if not currency_id:
            currency_id = 166
        currency = Currency(currency_id)
        return currency
    currency = property(get_fund_currency)

    def get_fund_bucket(self):
        bucket = self.fund_info['bucket'][0]
        return bucket
    bucket = property(get_fund_bucket)

    def get_fund_style(self):
        style = self.fund_info['style'][0]
        return style
    style = property(get_fund_style)

    def get_strategy(self):
        strategy = self.fund_info['strategy'][0]
        return strategy
    strategy = property(get_strategy)

    def get_fund_status(self, report_date=date.today()):
        fund_status = get_fund_attribute_by_date(self.id,
                                                 'fund_status',
                                                 report_date)
        return fund_status

    fund_status = property(get_fund_status)

    def get_legal_form(self, report_date=date.today()):
        legal_form = get_fund_attribute_by_date(self.id,
                                                'legal_form',
                                                report_date)
        return legal_form

    legal_form = property(get_legal_form)

    def get_sub_strategy(self):
        sub_strategy = \
            get_db_data(self.id, self.table_name, 'sub_strategy')
        return sub_strategy
    sub_strategy = property(get_sub_strategy)

    def get_fund_manager(self):
        agent_id = self.fund_info['fund_manager'][0]
        if agent_id:
            fund_manager = Agent(agent_id)
        else:
            fund_manager = None
        return fund_manager
    fund_manager = property(get_fund_manager)

    def get_fund_investment_manager(self):
        agent_id = self.fund_info['fund_investment_manager'][0]
        if agent_id:
            fund_investment_manager = Agent(agent_id)
        else:
            fund_investment_manager = None
        return fund_investment_manager
    fund_investment_manager = property(get_fund_investment_manager)

    def get_fund_admin(self):
        agent_id = self.fund_info['fund_admin'][0]
        if agent_id:
            fund_admin = Agent(agent_id)
        else:
            fund_admin = None
        return fund_admin
    fund_admin = property(get_fund_admin)

    def get_fund_transfer_agent(self):
        agent_id = self.fund_info['fund_transfer_agent'][0]
        if agent_id:
            fund_transfer_agent = Agent(agent_id)
        else:
            fund_transfer_agent = None
        return fund_transfer_agent
    fund_transfer_agent = property(get_fund_transfer_agent)

    def get_fund_prime_broker(self, report_date=date.today()):
        fund_prime_broker = get_fund_attribute_by_date(self.id,
                                                       'fund_prime_broker',
                                                       report_date)
        return fund_prime_broker

    fund_prime_broker = property(get_fund_prime_broker)

    def get_fund_custodian(self, report_date=date.today()):
        fund_custodian = get_fund_attribute_by_date(self.id,
                                                    'fund_custodian',
                                                    report_date)
        return fund_custodian
    fund_custodian = property(get_fund_custodian)

    def get_fund_legal_advisor(self, report_date=date.today()):
        fund_legal_advisor = \
            get_fund_attribute_by_date(self.id,
                                       'fund_legal_advisor',
                                       report_date)
        return fund_legal_advisor
    fund_legal_advisor = property(get_fund_legal_advisor)

    def get_fund_auditor(self, report_date=date.today()):
        fund_auditor = get_fund_attribute_by_date(self.id,
                                                  'fund_auditor',
                                                  report_date)
        return fund_auditor

    fund_auditor = property(get_fund_auditor)

    @property
    def benchmark_reporting(self):
        return Benchmark(self.fund_info['benchmark_reporting'][0])

    def get_benchmark_powerbi(self):
        pass

    def get_target_return(self):
        pass

    def get_active_positions(self):
        positions = DatabaseAPI.get_position_id_by_fund(self.id, 1)
        self.actives = [Position(position) for position in positions]
        return self.actives

    def get_passive_positions(self):
        positions = DatabaseAPI.get_position_id_by_fund(self.id, 0)
        self.passives = [Position(position) for position in positions]
        return self.passives

    def get_all_returns(self,
                        start_date=date(1900, 1, 1),
                        end_date=date(2100, 1, 1),
                        final=1):
        returns = []
        for position in self.passives:
            returns.append(position.security.get_mtd_returns(
                date_list=Helper.months_in_range(start_date, end_date),
                final=final))
        return returns
    returns = property(get_all_returns)

    def get_leading_series(self):
        """

        :return: returns DataFrame contains the longest series return from
        the fund
        """
        all_returns = self.get_all_returns(final=0)
        all_returns = [df for df in all_returns if df is not None]
        if not all_returns:
            return None
        leading_series = max(all_returns, key=len)
        return leading_series
    leading_series = property(get_leading_series)

    def calculate_returns_in_portfolio_currency(self, portfolio_libor):
        fund_libor = self.currency.libor.load_ticker_values('PX_LAST')
        self.returns_in_portfolio_currency = \
            self.leading_series.add(portfolio_libor).sub(
                fund_libor).dropna()

    def get_fund_history(self, field, report_date=date.today()):
        return DatabaseAPI.get_fund_history(self.id, field, report_date)


if __name__ == '__main__':
    fund = Fund(63)
    fund.get_leading_series()
    print("test")
