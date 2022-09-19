#!/usr/bin/env python3

import sqlite3

# import time

db_path = "/media/javier/wd500G_p1/tfg/cryto.db"
fecha_inicio = 20180101
fecha_fin = 20190101
hora_compra = 5
hora_venta = 23
exchange = 'krkn'
cryto = 'eth'
comision = 0.002


def main():
    print("begin")

    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    query = "select cast(strftime('%Y%m%d',time,'unixepoch') as integer) as fecha," \
            "cast(strftime('%H',time,'unixepoch') as integer) as hora,avg(open) " \
            "from tb" + exchange + cryto + "usd1m where fecha>=" + str(fecha_inicio) + " and fecha<=" + str(fecha_fin) + \
            " group by fecha,hora order by fecha,hora"
    cursor.execute(query)

    saldo = 1000
    inversion = 100
    operaciones_positivas = 0
    operaciones_negativas = 0
    # balance_usd = 0
    balance_eth = 0
    balance_saldo = 0
    for row in cursor.fetchall():
        balance_saldo_prev = balance_saldo
        #if int(row[1]) == hora_compra or int(row[1]) == hora_venta:
        #    print(f"{row[0]: <10},{row[1]: <3},{round(int(row[2]))},{operaciones_negativas},{operaciones_positivas},{round(balance_eth,4): <7},{saldo},{balance_saldo}")
        if int(row[1]) == hora_compra:
            saldo -= inversion
            balance_eth += inversion * (1 - comision) / float(row[2])
        if int(row[1]) == hora_venta:
            saldo += (float(row[2]) * balance_eth) * (1 - comision)
            balance_eth = 0
        balance_saldo = saldo + balance_eth * float(row[2])
        if int(row[1]) == hora_venta:
            if balance_saldo > balance_saldo_prev:
                operaciones_positivas += 1
            else:
                operaciones_negativas += 1
        if abs(int(row[0])) % 100 == 1 and int(row[1]) == hora_venta:
            print(f"{row[0]},{row[1]},{round(float(row[2]),4): <10},{operaciones_negativas: <3},{operaciones_positivas: <3},{balance_saldo}")

    con.close()

    print("end")


main()
