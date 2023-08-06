# import MySQLdb
import pymysql

# def connect():
#    db = MySQLdb.connect(host="172.16.17.22", port=3306, user='dev_user',
#                         passwd="dev_password", db="dev_db", charset='utf8',
#                         use_unicode=True)
#    return db


def connect():
    db = pymysql.connect('172.16.17.22', 'dev_user',
                         'dev_password', 'dev_db')
    return db
