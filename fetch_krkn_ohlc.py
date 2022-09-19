#!/usr/bin/env python3

# Importar datos de Kraken de tipo OHLC

# https://docs.kraken.com/rest/#tag/Market-Data/operation/getOHLCData

# Parámetros
# pair - XBTUSD, ETHUSD, LTCUSD
# interval - en minutos - default 1
# since - timestamp integer

# respuesta
# 720 elementos

import sqlite3
import time

from datetime import datetime, timedelta
from urllib3 import PoolManager
from json import loads

url_base = "https://api.kraken.com/0/public/OHLC?pair="
db_path = "/media/javier/disco500G_2/tfg/cryto.db"
#pairs = ['btcusd', 'ethusd', 'ltcusd']

def main():
    print("begin")

    date_start = datetime(2017, 1, 1)
    timestamp_start = int(date_start.timestamp())
    #date_stop = datetime(2022, 1, 1)
    date_stop = datetime(2017, 1, 2)
    timestamp_stop = int(date_stop.timestamp())
    # print(f"{date_start} # {timestamp_start}")
    timestamp_temp = int(timestamp_start)

    http = PoolManager()

    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    while timestamp_temp < timestamp_stop:
        url = url_base + "XBTUSD&since=" + str(timestamp_temp)
        print(url)
        # get de la url
        r = http.request('GET', url)
        # content = loads(r.data.decode('utf-8'))
        content = loads(r.data)
        for item in content['result']['XXBTZUSD']:
            #print(f"timestamp: {item[0]} open: {item[1]} high: {item[2]} low: {item[3]} close: {item[4]} volume: {item[6]}")
            try:
                cursor.execute("insert into tbkrknbtcusd1m (time,open,high,low,close,volume) values " +
                               "(" + str(item[0]) + "," + str(item[1]) + "," +
                               str(item[2]) + "," + str(item[3]) + "," +
                               str(item[4]) + "," + str(item[6]) + ");")
            except Exception as err:
                print('Query Failed: %s\nError: %s' % ("insert", str(err)))
        timestamp_temp += 60*720
        con.commit()
        time.sleep(5)

    con.close()

    print("end")


main()
