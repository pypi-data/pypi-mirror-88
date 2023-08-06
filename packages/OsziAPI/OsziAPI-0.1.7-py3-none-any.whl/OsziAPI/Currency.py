from OsziAPI.DatabaseAPI import get_db_data
from OsziAPI.Ticker import Ticker
from OsziAPI import DatabaseAPI


class Currency:
    def __init__(self, currency_id=None, currency_code=None):
        if currency_id:
            self.id = currency_id
        else:
            self.id = DatabaseAPI.get_currency_id_by_code(currency_code)
        self.name = self.get_currency_name()
        self.code = self.get_currency_code()
        self.libor = self.get_libor_ticker()

    def __str__(self):
        return self.name

    def get_currency_name(self):
        self.name = get_db_data(table='currencies', field='currency_name',
                                row_id=self.id)
        return self.name

    def get_currency_code(self):
        self.code = get_db_data(table='currencies', field='currency_code',
                                row_id=self.id)
        return self.code

    def get_libor_ticker(self):
        ticker_id = get_db_data(table='currencies', field='risk_free_rate_id',
                                row_id=self.id)
        self.libor = Ticker(ticker_id)
        return self.libor
