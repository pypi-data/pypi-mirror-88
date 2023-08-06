from OsziAPI.DatabaseAPI import get_db_data


class Country:
    def __init__(self, country_id):
        self.id = country_id
        self.name = self.get_country_name
        self.code = self.get_country_code

    def __str__(self):
        return self.name

    def get_country_name(self):
        self.name = get_db_data(table='country', field='country_name',
                                row_id=self.id)
        return self.name

    def get_country_code(self):
        self.code = get_db_data(table='country', field='country_code',
                                row_id=self.id)
        return self.code
