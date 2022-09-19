#!/usr/bin/env python

import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as md

db_path = "/media/javier/wd500G_p1/tfg/cryto.db"
timestamp_start = 1577836800
timestamp_end = 1609459200

query_krkn = "select strftime('%Y%m%d', datetime(time,'unixepoch')) as dia,min(time),avg(open) from tbkrknbtcusd1m where time>" + str(timestamp_start) + " and time<" + str(timestamp_end) + " group by dia limit 365;"
query_btfn = "select strftime('%Y%m%d', datetime(time,'unixepoch')) as dia,min(time),avg(open) from tbbtfnbtcusd1m where time>" + str(timestamp_start) + " and time<" + str(timestamp_end) + " group by dia limit 365;"
query_btst = "select strftime('%Y%m%d', datetime(time,'unixepoch')) as dia,min(time),avg(open) from tbbtstbtcusd1m where time>" + str(timestamp_start) + " and time<" + str(timestamp_end) + " group by dia limit 365;"
query_bnnc = "select strftime('%Y%m%d', datetime(time,'unixepoch')) as dia,min(time),avg(open) from tbbnncbtcusd1m where time>" + str(timestamp_start) + " and time<" + str(timestamp_end) + " group by dia limit 365;"

date = []
t = []
krkn = []
btfn = []
btst = []
bnnc = []

con = sqlite3.connect(db_path)
cursor = con.cursor()

cursor.execute(query_krkn)
for row in cursor.fetchall():
       date.append(int(row[0]))
       t.append(int(row[1]))
       krkn.append(float(row[2]))
print(t)

cursor.execute(query_btfn)
for row in cursor.fetchall():
       btfn.append(float(row[2]))

cursor.execute(query_krkn)
for row in cursor.fetchall():
       btst.append(float(row[2]))

cursor.execute(query_krkn)
for row in cursor.fetchall():
       bnnc.append(float(row[2]))

fig, ax = plt.subplots()
ax.plot(t, krkn, label="krkn")
ax.plot(t, btfn, label="btfn")
ax.plot(t, btst, label="btst")
ax.plot(t, bnnc, label="bnnc")
ax.legend()


ax.set(xlabel='fecha', ylabel='BTC/USD', title='Cotización de las 4 casas de cambio en 2020')
ax.grid()

fig.savefig("test.png")
plt.ticklabel_format(style='plain', axis="x")
plt.xticks(t[::15], date[::15], rotation=45)
plt.show()