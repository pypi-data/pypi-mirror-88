import datetime

from OsziAPI import DatabaseAPI


class Ticker:
    def __init__(self, ticker_id=None, bbg_ticker=None):
        if ticker_id:
            self.id = ticker_id
        else:
            self.id = DatabaseAPI.get_ticker_id_by_bbg_ticker(bbg_ticker)
        self.ticker_name = DatabaseAPI.get_db_data(row_id=self.id,
                                                   table='ticker',
                                                   field='ticker_name')
        self.bbg_ticker = DatabaseAPI.get_db_data(row_id=self.id,
                                                  table='ticker',
                                                  field='bloomberg_ticker')
        self.ticker_values = None

    def load_ticker_values(self, field='PX_LAST',
                           start_date=datetime.date(1900, 1, 1),
                           end_date=datetime.date(2100, 1, 1)):
        self.ticker_values = \
            DatabaseAPI.get_ticker_values(self.id,
                                          field,
                                          start_date,
                                          end_date) / 100
        return self.ticker_values
    
    @property
    def short_name(self):
        short_name = DatabaseAPI.get_db_data(row_id=self.id,
                                             table='ticker',
                                             field='ticker_short_name')
        if short_name:
            return short_name
        return self.ticker_name


if __name__ == '__main__':
    ticker = Ticker(77)
    ticker.load_ticker_values(field='PX_LAST',
                              start_date=datetime.date(2020, 1, 1),
                              end_date=datetime.date(2020, 10, 1),
                              )
