import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import requests
import  psycopg2
from psycopg2 import Error
import json
import ast
import numpy as np
import schedule
import time
import datetime as t


def get_data():

    sql_file1 = open('query/collection.sql')
    sql_file2 = open('query/expected_annual.sql')
    sql_file3 = open('query/expected_monthly.sql')
    sql_file4 = open('query/user_zone.sql')
    sql_file5 = open('query/group_products.sql')
    sql_text1 = sql_file1.read()
    sql_text2 = sql_file2.read()
    sql_text3 = sql_file3.read()
    sql_text4 = sql_file4.read()
    sql_text5 = sql_file5.read()
    try:
        connection = psycopg2.connect(user='postgres',
                                      password='3uyePAXP6J',
                                      host='212.47.226.25',
                                      port='5432',
                                      database='oolusolar_analytics')
        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print('You are Successfully connected to - ', record, '\n')
        if t.date.today().day == 1:
            df_paid= pd.read_sql_query(sql_text1, connection)
            df_paid.to_csv('Data/payments.csv', index=False)
            df_annual = pd.read_sql_query(sql_text2, connection)
            df_annual.to_csv('Data/annual.csv', index=False)
            df_monthly = pd.read_sql_query(sql_text3, connection)
            df_monthly.to_csv('Data/monthly.csv', index=False)
            df_zone = pd.read_sql_query(sql_text4, connection)
            df_zone.to_csv('Data/zones.csv', index=False)
            df_group = pd.read_sql_query(sql_text5, connection)
            df_group.to_csv('Data/group_products.csv', index=False)
            print('data updated')
    except (Exception, Error) as error:
        print(" Connection failed, try again", error)
        cursor.close()
    cursor.close()
    connection.close()

    return ''

# schedule.every().day.at("15:00").do(get_data)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)