#!/usr/bin/env python3

import sqlite3
import time

from datetime import datetime, timedelta
from urllib3 import PoolManager
from json import loads

url_base = "https://cex.io/api/ohlcv/hd/"
db_path = "/media/javier/disco500G_2/tfg/cryto.db"

def main():
    print("begin")

    date_start = datetime(2017, 1, 1)
    timestamp_start = int(date_start.timestamp())
    date_stop = datetime(2022, 1, 1)
    #date_stop = datetime(2017, 1, 2)
    timestamp_stop = int(date_stop.timestamp())
    # print(f"{date_start} # {timestamp_start}")
    timestamp_temp = int(timestamp_start)

    http = PoolManager()

    con = sqlite3.connect(db_path)
    cursor = con.cursor()


    while timestamp_temp < timestamp_stop:
        url = url_base + date_start.strftime("%Y%m%d") + "/btc/usd"
        print(url)
        # get de la url
        #r = http.request('GET', url)
        # content = loads(r.data.decode('utf-8'))
        #content = loads(r.data)
        #for item in content:
        #    print(f"timestamp: {item[0]} open: {item[1]} high: {item[2]} low: {item[3]} close: {item[4]} volume: {item[5]}")
        #    try:
        #        cursor.execute("insert into tbbtfnltcusd1m (time,open,high,low,close,volume) values " +
        #                       "(" + str(item[0]/1000) + "," + str(item[1]) + "," +
        #                       str(item[2]) + "," + str(item[3]) + "," +
        #                       str(item[4]) + "," + str(item[5]) + ");")
        #    except Exception as err:
        #        print('Query Failed: %s\nError: %s' % ("insert", str(err)))
        #    timestamp_temp = int(int(item[0])/1000)
        #timestamp_temp += 60*720
        #con.commit()
        time.sleep(2)

    con.close()

    # for _ in range(1826):
    #     print(date_start.strftime("%Y%m%d"))
    #
    #     # get de la url
    #     r = http.request('GET', url)
    #     cont = loads(r.data.decode('utf-8'))
    #     data = cont['data1m']
    #     # print(type(data))
    #     data_list = list(data[1:-1].split("],"))
    #     for item in data_list:
    #         info = item.replace('[', '').replace(']', '')
    #         trade = info.split(',')
    #         # print("time: " + trade[0] + " price: " + trade[1] + " volume: " + trade[5])
    #         # insertar en la base de datos
    #         try:
    #             cursor.execute(
    #                 "insert into " + db_tablename + " (time,open,low,high,close,volume) values (" + trade[0] + "," + trade[1] + "," + trade[2] + "," + trade[3] + "," + trade[4] + "," + trade[5] + ")")
    #         except Exception as err:
    #             print('Query Failed: %s\nError: %s' % ("insert", str(err)))
    #     con.commit()
    #     time.sleep(5)
    #     date_start += timedelta(days=1)

    print("end")


main()
