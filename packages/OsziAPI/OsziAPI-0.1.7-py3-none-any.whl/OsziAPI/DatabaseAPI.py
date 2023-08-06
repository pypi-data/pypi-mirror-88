import pandas as pd
import numpy as np
from OsziAPI import db_connection
from decimal import Decimal

db = db_connection.connect()


def get_report_setting_by_parameter(parameter):
    """
    :param parameter: report parameters: client name, output path etc.
    :return: string or float
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT value_string, value_float from report_settings where name=%s""",
                   (parameter,))
    value = cursor.fetchall()
    if value[0][0]:
        v = value[0][0]
    else:
        v = value[0][1]
    return v


def get_fund_id_by_client_id(client_id):
    cursor = db.cursor()
    cursor.execute("""
    SELECT fund_id from client_fund_basket where client_id=%s""", (client_id,))
    fund_id = cursor.fetchall()
    return fund_id


def get_client_id_by_client_name(client_name):
    cursor = db.cursor()
    cursor.execute(
        """SELECT id from client where client_name = %s""",
        (client_name,))
    currency = cursor.fetchone()
    if currency:
        return currency[0]
    return None


def get_currency_id_by_code(currency_code):
    """
    Get currency id by currency code
    :param currency_code:
    :return: currency id
    """
    cursor = db.cursor()
    cursor.execute(
        """SELECT id from currencies where currencies.currency_code = %s""",
        (currency_code,))
    currency = cursor.fetchone()
    if currency:
        return currency[0]
    return None


def get_ticker_id_by_bbg_ticker(bbg_ticker):
    """
    Get the ticker id by the Bloomberg ticker
    :param bbg_ticker: string, Bloomberg ticker
    :return:
    """
    cursor = db.cursor()
    cursor.execute(
        """SELECT id from ticker where bloomberg_ticker = %s""",
        (bbg_ticker,))
    ticker_id = cursor.fetchone()
    if ticker_id:
        return ticker_id[0]
    return None


def get_db_data(row_id, table, field):
    """
    Retrieve database data from certain table and datafield with id
    :param row_id: id in the table
    :param table: name of the table
    :param field: name of the field
    :return:
    """
    cursor = db.cursor()
    query = 'SELECT {} FROM {} WHERE {}'.format(field, table, 'id= ' + str(
        row_id))
    cursor.execute(query)
    data = cursor.fetchone()
    if data:
        return data[0]
    return None


def get_fund_history(fund_id, field, report_date):
    """
    Retrieve rows from table fund history with fund id
    :param fund_id:
    :param field:
    :param report_date:
    :return:
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM fund_history
    WHERE fund_id = %s
    AND attribute = %s
    AND value_date <= %s
    ORDER BY data_entry_date DESC
    LIMIT 1
    """, (fund_id, field, report_date))
    data = cursor.fetchone()
    if data:
        return data[0]
    return None


def get_fund_info(fund_id):
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM funds
        """)
    headers = cursor.fetchall()
    query = 'SELECT * FROM funds WHERE id={}'.format(fund_id)
    cursor.execute(query)
    data = cursor.fetchall()
    if data:
        return pd.DataFrame(list(data),
                            columns=[row[0] for row in headers])
    return None


def get_fund_id_by_hpid(hpid):
    cursor = db.cursor()
    cursor.execute("""
    SELECT id
    FROM funds
    WHERE hpid =%s
    """, (hpid,))
    data = cursor.fetchone()
    if data:
        return data[0]
    return None


def get_fund_attribute_by_date(fund_id, field, date):
    """
    Retrieve database data from certain table and datafield with id
    :param fund_id: id in the table
    :param field: name of the field
    :param date: name of the field
    :return:
    """
    cursor = db.cursor()
    query = 'SELECT string FROM fund_attribute ' \
            'WHERE fund_id={} ' \
            'AND attribute={} ' \
            'AND data_entry_date <= {} ' \
            'ORDER BY data_entry_date DESC'.format(fund_id,
                                                   '"' + field + '"',
                                                   '"' + str(date) + '"')
    cursor.execute(query)
    data = cursor.fetchone()
    if data:
        return data[0]
    return None


def get_fund_attribute_value_by_date(fund_id, field, date):
    """
    Retrieve database data from certain table and datafield with id
    :param fund_id: id in the table
    :param field: name of the field
    :param date: name of the field
    :return:
    """
    cursor = db.cursor()
    query = 'SELECT value FROM fund_attribute ' \
            'WHERE fund_id={} ' \
            'AND attribute={} ' \
            'AND data_entry_date <= {} ' \
            'ORDER BY data_entry_date DESC'.format(fund_id,
                                                   '"' + field + '"',
                                                   '"' + str(date) + '"')
    cursor.execute(query)
    data = cursor.fetchone()
    if data:
        return data[0]
    return None


def get_returns(security_id):
    """
    Retrieve rows from table returns with security id
    :param security_id:
    :return:
    """
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM returns
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT * 
    FROM returns
    WHERE security_id = %s
    """, (security_id,))
    returns = cursor.fetchall()
    df = pd.DataFrame(list(returns), columns=[row[0] for row in headers])
    return df


def get_end_mtd_returns(security_id):
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM end_mtd_ror
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT * 
    FROM end_mtd_ror
    WHERE security_id = %s
    """, (security_id,))
    returns = cursor.fetchall()
    df = pd.DataFrame(list(returns), columns=[row[0] for row in headers])
    return df


def get_end_mtd_ror(security_id, report_date, final):
    """
    Retrieve rows from table returns with security id
    :param security_id:
    :param report_date:
    :param final:
    :return:
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT value, value_date, final
    FROM end_mtd_ror
    WHERE security_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (security_id, report_date, final))
    returns = cursor.fetchone()
    if returns and returns[1].month == report_date.month:
        return returns
    elif returns:
        return [Decimal(np.NAN), returns[1], returns[2]]
    return [Decimal(np.NAN), None, None]


def get_end_ytd_ror(security_id, report_date, final):
    """
    Retrieve rows from table returns with security id
    :param security_id:
    :param report_date:
    :param final:
    :return:
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT value, value_date, final
    FROM end_ytd_ror
    WHERE security_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (security_id, report_date, final))
    returns = cursor.fetchone()
    if returns:
        return returns
    return [Decimal(np.NAN), None, None]


def get_end_y_ror(security_id, report_date, final):
    """
    Retrieve rows from table returns with security id
    :param security_id:
    :param report_date:
    :param final:
    :return:
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT value, value_date, final
    FROM end_y_ror
    WHERE security_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (security_id, report_date, final))
    returns = cursor.fetchone()
    if returns:
        return returns
    return [None, None, None]


def get_position_shares(position_id):
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM position_share_history
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT * 
    FROM position_share_history
    WHERE position_id = %s
    """, (position_id,))
    position_shares = cursor.fetchall()
    df = pd.DataFrame(list(position_shares), columns=[row[0]
                                                      for row in headers])
    return df


def get_end_price(security_id, final=0):
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM end_price
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT * 
    FROM end_price
    WHERE security_id = %s
    AND final >= %s
    """, (security_id, final,))
    end_prices = cursor.fetchall()
    df = pd.DataFrame(list(end_prices),
                      columns=[row[0] for row in headers])
    return df


def get_position_history(position_id, datafield):
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM positions_history
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT * 
    FROM positions_history
    WHERE position_id = %s
    AND data_type = %s
    """, (position_id, datafield,))
    position_history = cursor.fetchall()
    df = pd.DataFrame(list(position_history),
                      columns=[row[0] for row in headers])
    return df


def get_position_history_value(position_id, datafield, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM positions_history
    WHERE position_id = %s
    AND data_type = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    """, (position_id, datafield, report_date, final))
    position_history = cursor.fetchone()
    return position_history


def get_end_mv_base(position_id, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM end_mv_base
    WHERE position_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (position_id, report_date, final))
    position_history = cursor.fetchone()
    if position_history:
        return position_history[0]
    return Decimal(np.NAN)


def get_end_mv_date(position_id, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value_date
    FROM end_mv_base
    WHERE position_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (position_id, report_date, final))
    position_history = cursor.fetchone()
    if position_history:
        return position_history[0]
    return position_history


def get_end_mv_base_for_cont(position_id, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM end_mv_base_for_cont
    WHERE position_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (position_id, report_date, final))
    position_history = cursor.fetchone()
    if position_history:
        return position_history
    return [0]


def get_end_mv_base_adj_for_cont(position_id, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM end_mv_base_adj_for_cont
    WHERE position_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (position_id, report_date, final))
    position_history = cursor.fetchone()
    if position_history:
        return position_history
    return [0]


def get_end_mv_local(position_id, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM end_mv_local
    WHERE position_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (position_id, report_date, final))
    position_history = cursor.fetchone()
    if position_history:
        return position_history
    return [0]


def get_end_mv_local_for_cont(position_id, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM end_mv_local_for_cont
    WHERE position_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (position_id, report_date, final))
    position_history = cursor.fetchone()
    if position_history:
        return position_history
    return [0]


def get_end_mv_local_adj_for_cont(position_id, report_date, final):
    cursor = db.cursor()
    cursor.execute("""
    SELECT value
    FROM end_mv_local_adj_for_cont
    WHERE position_id = %s
    AND report_date = %s
    AND final >= %s
    ORDER BY value_date DESC, data_entry_date DESC, final DESC
    LIMIT 1
    """, (position_id, report_date, final))
    position_history = cursor.fetchone()
    if position_history:
        return position_history
    return [0]


def get_return_history(security_id, datafield):
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM returns
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT * 
    FROM returns
    WHERE security_id = %s
    AND return_type = %s
    """, (security_id, datafield,))
    return_history = cursor.fetchall()
    df = pd.DataFrame(list(return_history),
                      columns=[row[0] for row in headers])
    return df


def get_position_id_by_fund(fund_id, active=1):
    """
    Get position id by fund_id
    :param fund_id:
    :param active:
    :return:
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT id 
    FROM positions
    WHERE fund_id = %s
    AND active_passive = %s
    """, (fund_id, active,))
    returns = cursor.fetchall()
    positions = [row[0] for row in returns]
    return positions


def get_position_id_by_security_id(security_id, active=1):
    """
    Get position id by fund_id
    :param security_id:
    :param active:
    :return:
    """
    cursor = db.cursor()
    cursor.execute("""
    SELECT id 
    FROM positions
    WHERE series_id = %s
    AND active_passive = %s
    """, (security_id, active,))
    returns = cursor.fetchall()
    positions = [row[0] for row in returns]
    return positions


def get_ticker_values(ticker_id, field='PX_LAST', start_date=None,
                      end_date=None, report_date=None):
    """
    Get the values for the ticker id
    :param ticker_id: integer
    :param field: string field name, last price by default
    :param start_date: datetime
    :param end_date: datetime
    :param report_date: datetime
    :return:
    """
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM ticker_value
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT * 
    FROM ticker_value
    WHERE ticker_id = %s
    AND field = %s
    """, (ticker_id, field,))
    values = cursor.fetchall()
    df = pd.DataFrame(list(values), columns=[row[0] for row in headers])
    if report_date:
        df = df[df['data_entry_date'] <= pd.to_datetime(report_date)]
    date_list = pd.date_range(start_date, end_date, freq='1M')
    df = df[df['value_date'].isin(date_list)]
    df.sort_values(
        ['value_date', 'data_entry_date'],
        ascending=[True, False], inplace=True)
    return df.groupby('value_date').first()[['value']]


def get_benchmark_composition(benchmark_id):
    cursor = db.cursor()
    cursor.execute(
        """
        SHOW COLUMNS FROM benchmark_tickers_basket
        """)
    headers = cursor.fetchall()
    cursor.execute("""
    SELECT *
    FROM benchmark_tickers_basket
    WHERE benchmark_id = %s
    """, (float(benchmark_id),))
    values = cursor.fetchall()
    df = pd.DataFrame(list(values), columns=[row[0] for row in headers])
    return df


def get_all_tickers():
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT id from ticker
        """
    )
    tickers = cursor.fetchall()
    return tickers


def get_all_funds():
    cursor = db.cursor()
    cursor.execute(
        """
        SELECT id from funds
        """
    )
    funds = cursor.fetchall()
    return funds


def get_evestment_fund_id_by_name(fund_name):
    cursor = db.cursor()
    cursor.execute("""
    SELECT id 
    from funds
    where fund_name = %s
    AND evestment_id is not Null
    """, (fund_name,))
    fund_id = cursor.fetchone()
    if fund_id:
        return fund_id[0]
    return None
