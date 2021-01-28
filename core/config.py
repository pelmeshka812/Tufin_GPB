import sqlite3
from sqlite3 import Error
import datetime
import requests
import json
import base64

"""
def tufin_password():
        raw_password = '1q2w3e'
        password = base64.b85encode(raw_password.encode("utf-8"))
        return password

def createConnection():
    # Database File for SQLite
    # db_file = "core_database/tufin_reqs.db # Uncomment if running on Linux
    db_file = "C:\\Users\\chaudhary\\Documents\\tufin_py\\jang1\\core_database\\tufin_reqs.db" # Uncomment if running on windows
    create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
"""


def now():
    # Date Time Now
    now = (datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    return now
