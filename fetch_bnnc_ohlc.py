#!/usr/bin/env python3

import sqlite3
import time

from datetime import datetime
from urllib3 import PoolManager
from json import loads

# url ejemplo
# https://api.binance.com/api/v1/klines?symbol=BTCUSDT&interval=1m&startTime=1483228800000&limit=1500

url_base = "https://api.binance.com/api/v1/klines"
url_parametros = "?symbol=XRPUSDT&interval=1m&startTime="
db_path = "/media/javier/disco500G_2/tfg/cryto.db"

def main():
    print("begin")

    date_start = datetime(2017, 12, 12)
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
        url = url_base + url_parametros + str(timestamp_temp) + "000&limit=1500"
        print(url)
        # get de la url
        r = http.request('GET', url)
        # content = loads(r.data.decode('utf-8'))
        content = loads(r.data)
        for item in content:
            print(f"timestamp: {item[0]} open: {item[1]} high: {item[2]} low: {item[3]} close: {item[4]} volume: {item[5]}")
            try:
                cursor.execute("insert into tbbnncxrpusd1m (time,open,high,low,close,volume) values " +
                               "(" + str(item[0]/1000) + "," + str(item[1]) + "," +
                               str(item[2]) + "," + str(item[3]) + "," +
                               str(item[4]) + "," + str(item[5]) + ");")
            except Exception as err:
                print('Query Failed: %s\nError: %s' % ("insert", str(err)))
            timestamp_temp = int(int(item[0])/1000)
        #timestamp_temp += 60*720
        con.commit()
        time.sleep(2)

    for _ in range(10):
        print('\a')
        timestamp_temp.sleep(2)

    con.close()

    print("end")

main()

