#!/usr/bin/env python3

# Importar datos de Bitstamp de tipo OHLC

# API: https://www.bitstamp.net/api/#ohlc_data
# url: https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/
# pairs: Supported values for currency_pair: btcusd, btceur, btcgbp, btcpax, gbpusd, gbpeur, eurusd, xrpusd, xrpeur, xrpbtc, ...
#
# parámetros:
#   - start         unix timestamp
#   - end           unix timestamp
#   - step          intervalos en segundos. Posibles: 60, 180, 300, 900, 1800, 3600, ...
#   - limit         limite de resultados. [1-1000]
#
# respuesta:
#   Response (JSON): success - Returns a dictionary of tick data for selected trading pair.
#       Each tick in the dictionary is represented as a list of OHLC data.
#   - pair 	        Trading pair
#   - high 	        Price high
#   - timestamp 	Unix timestamp date and time
#   - volume 	    Volume
#   - low 	        Price low
#   - close 	    Closing price
#   - open 	        Opening price
#   Response (JSON): failure
#   - code 	"Error code"
#   - errors 	List with 'field', 'message' and 'code' fields.


import sqlite3
import time

from datetime import datetime, timedelta
from urllib3 import PoolManager
from json import loads


class DbHandler():
    def __init__(self, path="cryto.db", pairs=[]):
        self.con = sqlite3.connect(path)
        cursor = self.con.cursor()
        for pair in pairs:
            cursor.execute("create table if not exists tbbtst" + pair + "1m (" +
                           "time integer primary key," +
                           "open real, low real, high real, close real," +
                           "volume real);")
        self.con.commit()

    def _close(self):
        self.con.commit()
        self.con.close()


class FetchData():
    def __init__(self):
        pass


def main():
    print("begin")

    url_base = "https://www.bitstamp.net/api/v2/ohlc/"
    db_path = "/media/javier/disco500G_2/tfg/cryto.db"
    pairs = ['btcusd', 'ethusd', 'ltcusd']

    dh = DbHandler(db_path, pairs)

    date_start = datetime(2017, 1, 1)
    timestamp_start = int(date_start.timestamp())
    date_stop = datetime(2022, 1, 1)
    timestamp_stop = int(date_stop.timestamp())
    # print(f"{date_start} # {timestamp_start}")
    timestamp_temp = int(timestamp_start)

    http = PoolManager()
    cursor = dh.con.cursor()

    while timestamp_temp < timestamp_stop:
        url = url_base + "ltcusd" + "/?start=" + str(timestamp_temp) + "&step=60&limit=1000"
        print(url)
        # get de la url
        r = http.request('GET', url)
        # content = loads(r.data.decode('utf-8'))
        content = loads(r.data)
        if len(content['data']['ohlc']) == 0:
            timestamp_temp += 60*60*24
        else:
            for item in content['data']['ohlc']:
                print(
                    f"timestamp: {item['timestamp']} open: {item['open']} low: {item['low']} high: {item['high']} close: {item['close']} volume: {item['volume']}")
                try:
                    cursor.execute("insert into tbbtstltcusd1m (time,open,low,high,close,volume) values " +
                               "(" + str(item['timestamp']) + "," + str(item['open']) + "," +
                               str(item['low']) + "," + str(item['high']) + "," +
                               str(item['close']) + "," + str(item['volume']) + ");")
                except Exception as err:
                    print('Query Failed: %s\nError: %s' % ("insert", str(err)))
                timestamp_temp = int(item['timestamp'])
        time.sleep(2)

    dh._close()

    print("end")


main()
