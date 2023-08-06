import datetime
from datetime import timedelta
import pandas as pd


def months_in_range(start_date, end_date):
    """Get the last day of every month in a range between two datetime values.
    Return a generator
    """
    start_month = start_date.month
    end_months = (end_date.year-start_date.year)*12 + end_date.month

    date_list = []
    for month in range(start_month, end_months + 1):
        # Get years in the date range, add it to the start date's year
        year = int((month-1)/12) + start_date.year
        month = (month-1) % 12 + 1
        date_list.append(datetime.date(year, month, 1)-timedelta(days=1))
    return date_list


def convert_to_list(df):
    return [df.columns.tolist()] + df.reset_index().values.tolist()


def convert_to_list_woindex(df):
    return df.values.tolist()


def convert_to_isoformat(df):
    df.index = [i.isoformat() for i in df.index]
    return df


def cal_vami(self, df_input):
    df_input = df_input[self.incept_date:]
    cum = (df_input + 1).cumprod() - 1
    return cum * 100


def usd2chf(df):
    result = pd.DataFrame(index=df.index, columns=df.columns)
    if result.index[0].date() <= datetime.date(2018, 9, 30):
        result = result.combine_first(
            df.add(fx['SF0003M Index'] / 1200 - fx['US0003M Index'] / 1200, axis=0))[:'2018-9']
    after = ((df + 1).mul(fx['CHF L160 Curncy'] / fx['CHF L160 Curncy'].shift(1), axis=0) - 1).add(
        ((fx['CHF L160 Curncy'] + fx['SF1M L160 Curncy'] / 10000).shift(1) - fx['CHF L160 Curncy']) / fx[
            'CHF L160 Curncy'].shift(1), axis=0)['2018-10':]
    result = result.combine_first(after)

    return result.astype(float)