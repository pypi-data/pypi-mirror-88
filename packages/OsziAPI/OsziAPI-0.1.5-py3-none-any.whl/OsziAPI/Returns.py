
class RateOfReturn:
    def __init__(self, value, value_date, quality):
        self.value = value
        self.value_date = value_date
        self.quality = quality

    def __str__(self):
        return self.value

    def print_value_quality(self):
        if self.quality == 1:
            return 'Final'
        else:
            return 'Estimate'
