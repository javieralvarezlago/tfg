#!/usr/bin/env python3

# Check gaps en la base de datos
import sqlite3

from datetime import datetime

db_path = "/media/javier/disco500G_2/tfg/cryto.db"
table_name = "tbbtstltcusd1m"

def main():
    print("begin")
    print(db_path)
    print(table_name)
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    gap_max = 0
    gap_start = 0
    gap_end = 0
    time_prev = 0

    row = cursor.execute("select date(min(time), 'unixepoch'), date(max(time), 'unixepoch') from " + table_name + ";")
    print(row.fetchone())

    for row in cursor.execute("select * from " + table_name + " order by time"):
        if time_prev == 0:
            time_prev = int(row[0])
        elif int(row[0])-time_prev>gap_max:
            gap_max = int(row[0])-time_prev
            gap_start = time_prev
            gap_end = int(row[0])
        time_prev = int(row[0])

    con.close()

    print(f"{gap_start} {gap_end} {gap_max}s {gap_max/60}m")
    print(f"{datetime.fromtimestamp(gap_start)} - {datetime.fromtimestamp(gap_end)}")

    print("end")


main()