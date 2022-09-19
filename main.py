#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import pandas as pd
from tkinter import ttk

#import sqlite3
from time import time,sleep
from datetime import datetime

from DbHandler import *
from FetchData import *

class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("TFG: Inversiones")

        # barra de menus
        self.menubar = tk.Menu(self)

        self.menuarchivo = tk.Menu(self.menubar)
        self.menuarchivo.add_command(label="Salir")
        self.menuayuda = tk.Menu(self.menubar)
        self.menuayuda.add_command(label="Acerca de")

        self.menubar.add_cascade(label="Archivo", menu=self.menuarchivo)
        self.menubar.add_cascade(label="Edicion", menu=self.menuarchivo)
        self.menubar.add_cascade(label="Opciones", menu=self.menuarchivo)
        self.menubar.add_cascade(label="Ayuda", menu=self.menuayuda)

        main_window.config(menu=self.menubar)
    
        # Crear el panel de pestañas.
        self.notebook = ttk.Notebook(self)
        
        # Crear el contenido de cada una de las pestañas.
        self.dbestado_frame = tk.Frame()
        
        self.frame_hora = tk.LabelFrame(self.dbestado_frame,text="Hora")
        
        self.lhora_local = tk.Label(self.frame_hora,text="Hora local:")
        self.timestamp_local = tk.Entry(self.frame_hora)
        self.date_local = tk.Entry(self.frame_hora)
        self.timestamp_bupdate = tk.Button(self.frame_hora,text="sin datos", background="grey", command=self._get_server_timestamp)
        self.lhora_servidor = tk.Label(self.frame_hora,text="Hora servidor:")
        self.timestamp_servidor = tk.Entry(self.frame_hora)
        self.date_servidor = tk.Entry(self.frame_hora)
        
        self.lhora_local.grid(row=1,column=1)
        self.timestamp_local.grid(row=1,column=2)
        self.date_local.grid(row=1,column=3)
        self.timestamp_bupdate.grid(row=1,column=4,rowspan=2)
        self.lhora_servidor.grid(row=2,column=1)
        self.timestamp_servidor.grid(row=2,column=2)
        self.date_servidor.grid(row=2,column=3)
        
        self.frame_hora.pack()
                
        self.frame_kraken = tk.LabelFrame(self.dbestado_frame,text="Kraken")
        
        self.label_timestamp_min = tk.Label(self.frame_kraken, text="min(timestamp)")
        self.label_timestamp_max = tk.Label(self.frame_kraken, text="max(timestamp)")
        self.label_date_min = tk.Label(self.frame_kraken, text="min(fecha)")
        self.label_date_max = tk.Label(self.frame_kraken, text="max(fecha)")
        self.label_trades = tk.Label(self.frame_kraken, text="trades")
        self.kraken_btc_l01 = tk.Label(self.frame_kraken, text="BTC/USD")
        self.kraken_btc_e1 = tk.Entry(self.frame_kraken)
        self.kraken_btc_e2 = tk.Entry(self.frame_kraken)
        self.kraken_btc_e3 = tk.Entry(self.frame_kraken)
        self.kraken_btc_e4 = tk.Entry(self.frame_kraken)
        self.kraken_btc_e5 = tk.Entry(self.frame_kraken)
        self.kraken_btc_b1 = tk.Button(self.frame_kraken, text="sin datos", background="grey", command=self._get_db_state_krkn_btcusd)
        
        self.label_timestamp_min.grid(row=1,column="2")
        self.label_timestamp_max.grid(row=1,column="3")
        self.label_date_min.grid(row=1,column="4")
        self.label_date_max.grid(row=1,column="5")
        self.label_trades.grid(row=1,column="6")
        
        self.kraken_btc_l01.grid(row=2,column=1)
        self.kraken_btc_e1.grid(row=2,column=2)
        self.kraken_btc_e2.grid(row=2,column=3)
        self.kraken_btc_e3.grid(row=2,column=4)
        self.kraken_btc_e4.grid(row=2,column=5)
        self.kraken_btc_e5.grid(row=2,column=6)
        self.kraken_btc_b1.grid(row=2,column=7)
        
        self.kraken_eth_l01 = tk.Label(self.frame_kraken, text="ETH/USD")
        self.kraken_eth_e1 = tk.Entry(self.frame_kraken)
        self.kraken_eth_e2 = tk.Entry(self.frame_kraken)
        self.kraken_eth_e3 = tk.Entry(self.frame_kraken)
        self.kraken_eth_e4 = tk.Entry(self.frame_kraken)
        self.kraken_eth_e5 = tk.Entry(self.frame_kraken)
        self.kraken_eth_b1 = tk.Button(self.frame_kraken, text="sin datos", background="grey", command=self._get_db_state_krkn_ethusd)
        self.kraken_eth_l01.grid(row=3,column=1)
        self.kraken_eth_e1.grid(row=3,column=2)
        self.kraken_eth_e2.grid(row=3,column=3)
        self.kraken_eth_e3.grid(row=3,column=4)
        self.kraken_eth_e4.grid(row=3,column=5)
        self.kraken_eth_e5.grid(row=3,column=6)
        self.kraken_eth_b1.grid(row=3,column=7)

        self.kraken_ltc_l01 = tk.Label(self.frame_kraken, text="LTC/USD")
        self.kraken_ltc_e1 = tk.Entry(self.frame_kraken)
        self.kraken_ltc_e2 = tk.Entry(self.frame_kraken)
        self.kraken_ltc_e3 = tk.Entry(self.frame_kraken)
        self.kraken_ltc_e4 = tk.Entry(self.frame_kraken)
        self.kraken_ltc_e5 = tk.Entry(self.frame_kraken)
        self.kraken_ltc_b1 = tk.Button(self.frame_kraken, text="sin datos", background="grey", command=self._get_db_state_krkn_ltcusd)
        self.kraken_ltc_l01.grid(row=4,column=1)
        self.kraken_ltc_e1.grid(row=4,column=2)
        self.kraken_ltc_e2.grid(row=4,column=3)
        self.kraken_ltc_e3.grid(row=4,column=4)
        self.kraken_ltc_e4.grid(row=4,column=5)
        self.kraken_ltc_e5.grid(row=4,column=6)
        self.kraken_ltc_b1.grid(row=4,column=7)
        
        self.kraken_xrp_l01 = tk.Label(self.frame_kraken, text="XRP/USD")
        self.kraken_xrp_e1 = tk.Entry(self.frame_kraken)
        self.kraken_xrp_e2 = tk.Entry(self.frame_kraken)
        self.kraken_xrp_e3 = tk.Entry(self.frame_kraken)
        self.kraken_xrp_e4 = tk.Entry(self.frame_kraken)
        self.kraken_xrp_e5 = tk.Entry(self.frame_kraken)
        self.kraken_xrp_b1 = tk.Button(self.frame_kraken, text="sin datos", background="grey", command=self._get_db_state_krkn_xrpusd)
        self.kraken_xrp_l01.grid(row=5,column=1)
        self.kraken_xrp_e1.grid(row=5,column=2)
        self.kraken_xrp_e2.grid(row=5,column=3)
        self.kraken_xrp_e3.grid(row=5,column=4)
        self.kraken_xrp_e4.grid(row=5,column=5)
        self.kraken_xrp_e5.grid(row=5,column=6)
        self.kraken_xrp_b1.grid(row=5,column=7)
        
        self.frame_kraken.pack()

        self.frame_bitfinex = tk.LabelFrame(self.dbestado_frame,text="Bitfinex")

        self.bitfinex_btc_l01 = tk.Label(self.frame_bitfinex, text="BTC/USD")
        self.bitfinex_btc_e1 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_btc_e2 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_btc_e3 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_btc_e4 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_btc_e5 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_btc_b1 = tk.Button(self.frame_bitfinex, text="sin datos", background="grey", command=self._get_db_state_btfn_btcusd)
        self.bitfinex_btc_l01.grid(row=1,column=1)
        self.bitfinex_btc_e1.grid(row=1,column=2)
        self.bitfinex_btc_e2.grid(row=1,column=3)
        self.bitfinex_btc_e3.grid(row=1,column=4)
        self.bitfinex_btc_e4.grid(row=1,column=5)
        self.bitfinex_btc_e5.grid(row=1,column=6)
        self.bitfinex_btc_b1.grid(row=1,column=7)

        self.bitfinex_eth_l01 = tk.Label(self.frame_bitfinex, text="ETH/USD")
        self.bitfinex_eth_e1 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_eth_e2 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_eth_e3 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_eth_e4 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_eth_e5 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_eth_b1 = tk.Button(self.frame_bitfinex, text="sin datos", background="grey", command=self._get_db_state_btfn_ethusd)
        self.bitfinex_eth_l01.grid(row=2,column=1)
        self.bitfinex_eth_e1.grid(row=2,column=2)
        self.bitfinex_eth_e2.grid(row=2,column=3)
        self.bitfinex_eth_e3.grid(row=2,column=4)
        self.bitfinex_eth_e4.grid(row=2,column=5)
        self.bitfinex_eth_e5.grid(row=2,column=6)
        self.bitfinex_eth_b1.grid(row=2,column=7)

        self.bitfinex_ltc_l01 = tk.Label(self.frame_bitfinex, text="LTC/USD")
        self.bitfinex_ltc_e1 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_ltc_e2 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_ltc_e3 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_ltc_e4 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_ltc_e5 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_ltc_b1 = tk.Button(self.frame_bitfinex, text="sin datos", background="grey", command=self._get_db_state_btfn_ltcusd)
        self.bitfinex_ltc_l01.grid(row=3,column=1)
        self.bitfinex_ltc_e1.grid(row=3,column=2)
        self.bitfinex_ltc_e2.grid(row=3,column=3)
        self.bitfinex_ltc_e3.grid(row=3,column=4)
        self.bitfinex_ltc_e4.grid(row=3,column=5)
        self.bitfinex_ltc_e5.grid(row=3,column=6)
        self.bitfinex_ltc_b1.grid(row=3,column=7)
        
        self.bitfinex_xrp_l01 = tk.Label(self.frame_bitfinex, text="XRP/USD")
        self.bitfinex_xrp_e1 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_xrp_e2 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_xrp_e3 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_xrp_e4 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_xrp_e5 = tk.Entry(self.frame_bitfinex)
        self.bitfinex_xrp_b1 = tk.Button(self.frame_bitfinex, text="sin datos", background="grey", command=self._get_db_state_btfn_xrpusd)
        self.bitfinex_xrp_l01.grid(row=4,column=1)
        self.bitfinex_xrp_e1.grid(row=4,column=2)
        self.bitfinex_xrp_e2.grid(row=4,column=3)
        self.bitfinex_xrp_e3.grid(row=4,column=4)
        self.bitfinex_xrp_e4.grid(row=4,column=5)
        self.bitfinex_xrp_e5.grid(row=4,column=6)
        self.bitfinex_xrp_b1.grid(row=4,column=7)
        
        self.frame_bitfinex.pack()

        self.frame_bitstamp = tk.LabelFrame(self.dbestado_frame,text="Bitstamp")

        self.bitstamp_btc_l01 = tk.Label(self.frame_bitstamp, text="BTC/USD")
        self.bitstamp_btc_e1 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_btc_e2 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_btc_e3 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_btc_e4 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_btc_e5 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_btc_b1 = tk.Button(self.frame_bitstamp, text="sin datos", background="grey", command=self._get_db_state_btst_btcusd)
        self.bitstamp_btc_l01.grid(row=1,column=1)
        self.bitstamp_btc_e1.grid(row=1,column=2)
        self.bitstamp_btc_e2.grid(row=1,column=3)
        self.bitstamp_btc_e3.grid(row=1,column=4)
        self.bitstamp_btc_e4.grid(row=1,column=5)
        self.bitstamp_btc_e5.grid(row=1,column=6)
        self.bitstamp_btc_b1.grid(row=1,column=7)

        self.bitstamp_eth_l01 = tk.Label(self.frame_bitstamp, text="ETH/USD")
        self.bitstamp_eth_e1 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_eth_e2 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_eth_e3 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_eth_e4 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_eth_e5 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_eth_b1 = tk.Button(self.frame_bitstamp, text="sin datos", background="grey", command=self._get_db_state_btst_ethusd)
        self.bitstamp_eth_l01.grid(row=2,column=1)
        self.bitstamp_eth_e1.grid(row=2,column=2)
        self.bitstamp_eth_e2.grid(row=2,column=3)
        self.bitstamp_eth_e3.grid(row=2,column=4)
        self.bitstamp_eth_e4.grid(row=2,column=5)
        self.bitstamp_eth_e5.grid(row=2,column=6)
        self.bitstamp_eth_b1.grid(row=2,column=7)

        self.bitstamp_ltc_l01 = tk.Label(self.frame_bitstamp, text="LTC/USD")
        self.bitstamp_ltc_e1 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_ltc_e2 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_ltc_e3 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_ltc_e4 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_ltc_e5 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_ltc_b1 = tk.Button(self.frame_bitstamp, text="sin datos", background="grey", command=self._get_db_state_btst_ltcusd)
        self.bitstamp_ltc_l01.grid(row=3,column=1)
        self.bitstamp_ltc_e1.grid(row=3,column=2)
        self.bitstamp_ltc_e2.grid(row=3,column=3)
        self.bitstamp_ltc_e3.grid(row=3,column=4)
        self.bitstamp_ltc_e4.grid(row=3,column=5)
        self.bitstamp_ltc_e5.grid(row=3,column=6)
        self.bitstamp_ltc_b1.grid(row=3,column=7)

        self.bitstamp_xrp_l01 = tk.Label(self.frame_bitstamp, text="XRP/USD")
        self.bitstamp_xrp_e1 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_xrp_e2 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_xrp_e3 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_xrp_e4 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_xrp_e5 = tk.Entry(self.frame_bitstamp)
        self.bitstamp_xrp_b1 = tk.Button(self.frame_bitstamp, text="sin datos", background="grey", command=self._get_db_state_btst_xrpusd)
        self.bitstamp_xrp_l01.grid(row=4,column=1)
        self.bitstamp_xrp_e1.grid(row=4,column=2)
        self.bitstamp_xrp_e2.grid(row=4,column=3)
        self.bitstamp_xrp_e3.grid(row=4,column=4)
        self.bitstamp_xrp_e4.grid(row=4,column=5)
        self.bitstamp_xrp_e5.grid(row=4,column=6)
        self.bitstamp_xrp_b1.grid(row=4,column=7)

        self.frame_bitstamp.pack()

        self.frame_binance = tk.LabelFrame(self.dbestado_frame,text="Binance")

        self.binance_btc_l01 = tk.Label(self.frame_binance, text="BTC/USD")
        self.binance_btc_e1 = tk.Entry(self.frame_binance)
        self.binance_btc_e2 = tk.Entry(self.frame_binance)
        self.binance_btc_e3 = tk.Entry(self.frame_binance)
        self.binance_btc_e4 = tk.Entry(self.frame_binance)
        self.binance_btc_e5 = tk.Entry(self.frame_binance)
        self.binance_btc_b1 = tk.Button(self.frame_binance, text="sin datos", background="grey", command=self._get_db_state_bnnc_btcusd)
        self.binance_btc_l01.grid(row=1,column=1)
        self.binance_btc_e1.grid(row=1,column=2)
        self.binance_btc_e2.grid(row=1,column=3)
        self.binance_btc_e3.grid(row=1,column=4)
        self.binance_btc_e4.grid(row=1,column=5)
        self.binance_btc_e5.grid(row=1,column=6)
        self.binance_btc_b1.grid(row=1,column=7)

        self.binance_eth_l01 = tk.Label(self.frame_binance, text="ETH/USD")
        self.binance_eth_e1 = tk.Entry(self.frame_binance)
        self.binance_eth_e2 = tk.Entry(self.frame_binance)
        self.binance_eth_e3 = tk.Entry(self.frame_binance)
        self.binance_eth_e4 = tk.Entry(self.frame_binance)
        self.binance_eth_e5 = tk.Entry(self.frame_binance)
        self.binance_eth_b1 = tk.Button(self.frame_binance, text="sin datos", background="grey", command=self._get_db_state_bnnc_ethusd)
        self.binance_eth_l01.grid(row=2,column=1)
        self.binance_eth_e1.grid(row=2,column=2)
        self.binance_eth_e2.grid(row=2,column=3)
        self.binance_eth_e3.grid(row=2,column=4)
        self.binance_eth_e4.grid(row=2,column=5)
        self.binance_eth_e5.grid(row=2,column=6)
        self.binance_eth_b1.grid(row=2,column=7)

        self.binance_ltc_l01 = tk.Label(self.frame_binance, text="LTC/USD")
        self.binance_ltc_e1 = tk.Entry(self.frame_binance)
        self.binance_ltc_e2 = tk.Entry(self.frame_binance)
        self.binance_ltc_e3 = tk.Entry(self.frame_binance)
        self.binance_ltc_e4 = tk.Entry(self.frame_binance)
        self.binance_ltc_e5 = tk.Entry(self.frame_binance)
        self.binance_ltc_b1 = tk.Button(self.frame_binance, text="sin datos", background="grey", command=self._get_db_state_bnnc_ltcusd)
        self.binance_ltc_l01.grid(row=3,column=1)
        self.binance_ltc_e1.grid(row=3,column=2)
        self.binance_ltc_e2.grid(row=3,column=3)
        self.binance_ltc_e3.grid(row=3,column=4)
        self.binance_ltc_e4.grid(row=3,column=5)
        self.binance_ltc_e5.grid(row=3,column=6)
        self.binance_ltc_b1.grid(row=3,column=7)

        self.binance_xrp_l01 = tk.Label(self.frame_binance, text="XRP/USD")
        self.binance_xrp_e1 = tk.Entry(self.frame_binance)
        self.binance_xrp_e2 = tk.Entry(self.frame_binance)
        self.binance_xrp_e3 = tk.Entry(self.frame_binance)
        self.binance_xrp_e4 = tk.Entry(self.frame_binance)
        self.binance_xrp_e5 = tk.Entry(self.frame_binance)
        self.binance_xrp_b1 = tk.Button(self.frame_binance, text="sin datos", background="grey", command=self._get_db_state_bnnc_xrpusd)
        self.binance_xrp_l01.grid(row=4,column=1)
        self.binance_xrp_e1.grid(row=4,column=2)
        self.binance_xrp_e2.grid(row=4,column=3)
        self.binance_xrp_e3.grid(row=4,column=4)
        self.binance_xrp_e4.grid(row=4,column=5)
        self.binance_xrp_e5.grid(row=4,column=6)
        self.binance_xrp_b1.grid(row=4,column=7)
       
        self.frame_binance.pack()
        
        self.frame_acciones = tk.LabelFrame(self.dbestado_frame,text="Acciones")
        
        self.dbacciones_frame = tk.Frame(self.frame_acciones);
        self.dbacciones_actualizar = tk.Button(self.dbacciones_frame,text="Actualizar", command=self._fetch_data)
        self.dbacciones_actualizar_loop = ttk.Checkbutton(self.dbacciones_frame,text="bucle")
        self.dbacciones_actualizar.grid(row="1",column="1")
        self.dbacciones_actualizar_loop.grid(row="1",column="2")
        self.dbacciones_frame.pack()
        self.frame_acciones.pack()

        self.dbestado_frame.pack()
        
        # db consultas
        self.dbconsultas_frame = tk.Frame()
        
        self.dbconsultas_consulta_frame = tk.LabelFrame(self.dbconsultas_frame,text="Consulta")
        self.dbconsultas_consulta_text = tk.Text(self.dbconsultas_consulta_frame, height = 5, width = 80)
        self.dbconsultas_consulta_text.pack()
        self.dbconsultas_consulta_frame.pack()
        
        self.dbconsultas_errores_frame = tk.LabelFrame(self.dbconsultas_frame,text="Errores")
        self.dbconsultas_errores_text = tk.Text(self.dbconsultas_errores_frame, height = 5, width = 80)
        self.dbconsultas_errores_text.pack()
        self.dbconsultas_errores_frame.pack()
        
        self.dbconsultas_acciones_frame = tk.LabelFrame(self.dbconsultas_frame,text="Acciones")
        self.dbconsultas_acciones_bejecutar = tk.Button(self.dbconsultas_acciones_frame, text="Ejecutar")
        self.dbconsultas_acciones_bborrar = tk.Button(self.dbconsultas_acciones_frame, text="Borrar")
        self.dbconsultas_acciones_bejecutar.grid(row="1",column="1")
        self.dbconsultas_acciones_bborrar.grid(row="1",column="2")
        self.dbconsultas_acciones_frame.pack()
        
        self.dbconsultas_resultado_frame = tk.LabelFrame(self.dbconsultas_frame,text="Resultado")
        self.dbconsultas_resultado_treeview = ttk.Treeview(self.dbconsultas_resultado_frame)
        self.dbconsultas_resultado_treeview.pack()
        self.dbconsultas_resultado_frame.pack()
        
        self.dbconsultas_frame.pack()
        
        # Tab de Graficos
        self.graficos_frame = tk.Frame()
        
        self.graficos_datos_frame = tk.LabelFrame(self.graficos_frame,text="Datos")
        self.graficos_lkraken = tk.Label(self.graficos_datos_frame,text="Kraken")
        self.graficos_kraken_btcusd = ttk.Checkbutton(self.graficos_datos_frame, text="BTC/USD")
        self.graficos_kraken_ethusd = ttk.Checkbutton(self.graficos_datos_frame, text="ETH/USD")
        self.graficos_kraken_ltcusd = ttk.Checkbutton(self.graficos_datos_frame, text="LTC/USD")
        self.graficos_lkraken.grid(row="1",column="1")
        self.graficos_kraken_btcusd.grid(row="2",column="1")
        self.graficos_kraken_ethusd.grid(row="2",column="2")
        self.graficos_kraken_ltcusd.grid(row="2",column="3")
        
        self.graficos_lbitstamp = tk.Label(self.graficos_datos_frame,text="Bitstamp")
        self.graficos_bitstamp_btcusd = ttk.Checkbutton(self.graficos_datos_frame, text="BTC/USD")
        self.graficos_bitstamp_ethusd = ttk.Checkbutton(self.graficos_datos_frame, text="ETH/USD")
        self.graficos_bitstamp_ltcusd = ttk.Checkbutton(self.graficos_datos_frame, text="LTC/USD")
        self.graficos_lbitstamp.grid(row="3",column="1")
        self.graficos_bitstamp_btcusd.grid(row="4",column="1")
        self.graficos_bitstamp_ethusd.grid(row="4",column="2")
        self.graficos_bitstamp_ltcusd.grid(row="4",column="3")
        
        
        self.graficos_datos_frame.pack()
        
        
        self.graficos_frame.pack()
        
        
        # Provisional
        self.lcartera = ttk.Label(self.notebook, text="Cartera")
        self.lsimulador = ttk.Label(self.notebook, text="Simulador")
        
        # Añadirlas al panel con su respectivo texto.
        self.notebook.add(self.dbestado_frame, text="BD estado")
        self.notebook.add(self.dbconsultas_frame, text="BD consultas")
        self.notebook.add(self.graficos_frame, text="Graficos")
        self.notebook.add(self.lcartera, text="Cartera")
        self.notebook.add(self.lsimulador, text="Simulador")
        
        self.notebook.pack(fill=tk.X)
        
        # Ventana inferior de log
        self.text = tk.Text(self, height = 5, width = 80)
        self.text.pack()
        
        # Status Bar
        statusbar = tk.Label(self, text="barra de estado ...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        #self.geometry("400x400")
        self.pack()

    ## Funcionalidades ##

    def _get_server_timestamp(self):
        now = time()
        self.timestamp_local.delete(0,tk.END)
        self.timestamp_local.insert(0, str(now))
        self.date_local.delete(0,tk.END)
        self.date_local.insert(0,datetime.fromtimestamp(now))
        fd = FetchData()
        timestamp_server = fd._fetch_krkn_timestamp()
        self.timestamp_servidor.delete(0, tk.END)
        self.timestamp_servidor.insert(0, str(timestamp_server))
        self.date_servidor.delete(0, tk.END)
        self.date_servidor.insert(0, datetime.fromtimestamp(timestamp_server))
        if abs(now-timestamp_server)<600:
            self.timestamp_bupdate.configure(background="green")
            self.timestamp_bupdate.configure(text="en hora")
        elif abs(now-timestamp_server)<3600:
            self.timestamp_bupdate.configure(background="yellow")
            self.timestamp_bupdate.configure(text="retraso")
        else:
            self.timestamp_bupdate.configure(background="red")
            self.timestamp_bupdate.configure(text="error")

    def _get_db_state_krkn_btcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando kraken btcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("krkn","btcusd")
        db._close()
        self.kraken_btc_e1.delete(0, tk.END)
        self.kraken_btc_e1.insert(0, str(time_min))
        self.kraken_btc_e3.delete(0, tk.END)
        self.kraken_btc_e3.insert(0, str(time_max))
        self.kraken_btc_e2.delete(0, tk.END)
        self.kraken_btc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.kraken_btc_e4.delete(0, tk.END)
        self.kraken_btc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.kraken_btc_e5.delete(0, tk.END)
        self.kraken_btc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.kraken_btc_b1.configure(background="green",text="sincronizado")
        else:
            self.kraken_btc_b1.configure(background="red",text="desactualizado")
    
    def _fetch_kraken_btcusd(self):
        fd = FetchData()
        fd._fetch_krkn("btcusd","XXBTZUSD")
        print(fb)
    
    def _get_db_state_krkn_ethusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando kraken ethusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("krkn","ethusd")
        db._close()
        self.kraken_eth_e1.delete(0, tk.END)
        self.kraken_eth_e1.insert(0, str(time_min))
        self.kraken_eth_e3.delete(0, tk.END)
        self.kraken_eth_e3.insert(0, str(time_max))
        self.kraken_eth_e2.delete(0, tk.END)
        self.kraken_eth_e2.insert(0, datetime.fromtimestamp(time_min))
        self.kraken_eth_e4.delete(0, tk.END)
        self.kraken_eth_e4.insert(0, datetime.fromtimestamp(time_max))
        self.kraken_eth_e5.delete(0, tk.END)
        self.kraken_eth_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.kraken_eth_b1.configure(background="green",text="sincronizado")
        else:
            self.kraken_eth_b1.configure(background="red",text="desactualizado")
    
    def _get_db_state_krkn_ltcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando kraken ltcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("krkn","ltcusd")
        db._close()
        self.kraken_ltc_e1.delete(0, tk.END)
        self.kraken_ltc_e1.insert(0, str(time_min))
        self.kraken_ltc_e3.delete(0, tk.END)
        self.kraken_ltc_e3.insert(0, str(time_max))
        self.kraken_ltc_e2.delete(0, tk.END)
        self.kraken_ltc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.kraken_ltc_e4.delete(0, tk.END)
        self.kraken_ltc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.kraken_ltc_e5.delete(0, tk.END)
        self.kraken_ltc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.kraken_ltc_b1.configure(background="green",text="sincronizado")
        else:
            self.kraken_ltc_b1.configure(background="red",text="desactualizado")
    
    def _get_db_state_krkn_xrpusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando kraken xrpusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("krkn","xrpusd")
        db._close()
        self.kraken_xrp_e1.delete(0, tk.END)
        self.kraken_xrp_e1.insert(0, str(time_min))
        self.kraken_xrp_e3.delete(0, tk.END)
        self.kraken_xrp_e3.insert(0, str(time_max))
        self.kraken_xrp_e2.delete(0, tk.END)
        self.kraken_xrp_e2.insert(0, datetime.fromtimestamp(time_min))
        self.kraken_xrp_e4.delete(0, tk.END)
        self.kraken_xrp_e4.insert(0, datetime.fromtimestamp(time_max))
        self.kraken_xrp_e5.delete(0, tk.END)
        self.kraken_xrp_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.kraken_xrp_b1.configure(background="green",text="sincronizado")
        else:
            self.kraken_xrp_b1.configure(background="red",text="desactualizado")

    def _get_db_state_btfn_btcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitfinex btcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btfn","btcusd")
        # milisegundos
        #time_min /= 1000
        #time_max /= 1000
        db._close()
        self.bitfinex_btc_e1.delete(0, tk.END)
        self.bitfinex_btc_e1.insert(0, str(time_min))
        self.bitfinex_btc_e3.delete(0, tk.END)
        self.bitfinex_btc_e3.insert(0, str(time_max))
        self.bitfinex_btc_e2.delete(0, tk.END)
        self.bitfinex_btc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitfinex_btc_e4.delete(0, tk.END)
        self.bitfinex_btc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitfinex_btc_e5.delete(0, tk.END)
        self.bitfinex_btc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitfinex_btc_b1.configure(background="green",text="sincronizado")
        else:
            self.bitfinex_btc_b1.configure(background="red",text="desactualizado")

    def _get_db_state_btfn_ethusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitfinex ethusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btfn","ethusd")
        # milisegundos
        #time_min /= 1000
        #time_max /= 1000
        db._close()
        self.bitfinex_eth_e1.delete(0, tk.END)
        self.bitfinex_eth_e1.insert(0, str(time_min))
        self.bitfinex_eth_e3.delete(0, tk.END)
        self.bitfinex_eth_e3.insert(0, str(time_max))
        self.bitfinex_eth_e2.delete(0, tk.END)
        self.bitfinex_eth_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitfinex_eth_e4.delete(0, tk.END)
        self.bitfinex_eth_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitfinex_eth_e5.delete(0, tk.END)
        self.bitfinex_eth_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitfinex_eth_b1.configure(background="green",text="sincronizado")
        else:
            self.bitfinex_eth_b1.configure(background="red",text="desactualizado")

    def _get_db_state_btfn_ltcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitfinex ltcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btfn","ltcusd")
        # milisegundos
        #time_min /= 1000
        #time_max /= 1000
        db._close()
        self.bitfinex_ltc_e1.delete(0, tk.END)
        self.bitfinex_ltc_e1.insert(0, str(time_min))
        self.bitfinex_ltc_e3.delete(0, tk.END)
        self.bitfinex_ltc_e3.insert(0, str(time_max))
        self.bitfinex_ltc_e2.delete(0, tk.END)
        self.bitfinex_ltc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitfinex_ltc_e4.delete(0, tk.END)
        self.bitfinex_ltc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitfinex_ltc_e5.delete(0, tk.END)
        self.bitfinex_ltc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitfinex_ltc_b1.configure(background="green",text="sincronizado")
        else:
            self.bitfinex_ltc_b1.configure(background="red",text="desactualizado")

    def _get_db_state_btfn_xrpusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitfinex xrpusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btfn","xrpusd")
        # milisegundos
        #time_min /= 1000
        #time_max /= 1000
        db._close()
        self.bitfinex_xrp_e1.delete(0, tk.END)
        self.bitfinex_xrp_e1.insert(0, str(time_min))
        self.bitfinex_xrp_e3.delete(0, tk.END)
        self.bitfinex_xrp_e3.insert(0, str(time_max))
        self.bitfinex_xrp_e2.delete(0, tk.END)
        self.bitfinex_xrp_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitfinex_xrp_e4.delete(0, tk.END)
        self.bitfinex_xrp_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitfinex_xrp_e5.delete(0, tk.END)
        self.bitfinex_xrp_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitfinex_xrp_b1.configure(background="green",text="sincronizado")
        else:
            self.bitfinex_xrp_b1.configure(background="red",text="desactualizado")

    def _get_db_state_btst_btcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitstamp btcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btst","btcusd")
        db._close()
        self.bitstamp_btc_e1.delete(0, tk.END)
        self.bitstamp_btc_e1.insert(0, str(time_min))
        self.bitstamp_btc_e3.delete(0, tk.END)
        self.bitstamp_btc_e3.insert(0, str(time_max))
        self.bitstamp_btc_e2.delete(0, tk.END)
        self.bitstamp_btc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitstamp_btc_e4.delete(0, tk.END)
        self.bitstamp_btc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitstamp_btc_e5.delete(0, tk.END)
        self.bitstamp_btc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitstamp_btc_b1.configure(background="green",text="sincronizado")
        else:
            self.bitstamp_btc_b1.configure(background="red",text="desactualizado")

    def _get_db_state_btst_ethusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitstamp ethusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btst","ethusd")
        db._close()
        self.bitstamp_eth_e1.delete(0, tk.END)
        self.bitstamp_eth_e1.insert(0, str(time_min))
        self.bitstamp_eth_e3.delete(0, tk.END)
        self.bitstamp_eth_e3.insert(0, str(time_max))
        self.bitstamp_eth_e2.delete(0, tk.END)
        self.bitstamp_eth_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitstamp_eth_e4.delete(0, tk.END)
        self.bitstamp_eth_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitstamp_eth_e5.delete(0, tk.END)
        self.bitstamp_eth_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitstamp_eth_b1.configure(background="green",text="sincronizado")
        else:
            self.bitstamp_eth_b1.configure(background="red",text="desactualizado")


    def _get_db_state_btst_ltcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitfinex ltcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btst","ltcusd")
        db._close()
        self.bitstamp_ltc_e1.delete(0, tk.END)
        self.bitstamp_ltc_e1.insert(0, str(time_min))
        self.bitstamp_ltc_e3.delete(0, tk.END)
        self.bitstamp_ltc_e3.insert(0, str(time_max))
        self.bitstamp_ltc_e2.delete(0, tk.END)
        self.bitstamp_ltc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitstamp_ltc_e4.delete(0, tk.END)
        self.bitstamp_ltc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitstamp_ltc_e5.delete(0, tk.END)
        self.bitstamp_ltc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitstamp_ltc_b1.configure(background="green",text="sincronizado")
        else:
            self.bitstamp_ltc_b1.configure(background="red",text="desactualizado")

    def _get_db_state_btst_xrpusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando bitfinex xrpusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("btst","xrpusd")
        db._close()
        self.bitstamp_xrp_e1.delete(0, tk.END)
        self.bitstamp_xrp_e1.insert(0, str(time_min))
        self.bitstamp_xrp_e3.delete(0, tk.END)
        self.bitstamp_xrp_e3.insert(0, str(time_max))
        self.bitstamp_xrp_e2.delete(0, tk.END)
        self.bitstamp_xrp_e2.insert(0, datetime.fromtimestamp(time_min))
        self.bitstamp_xrp_e4.delete(0, tk.END)
        self.bitstamp_xrp_e4.insert(0, datetime.fromtimestamp(time_max))
        self.bitstamp_xrp_e5.delete(0, tk.END)
        self.bitstamp_xrp_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.bitstamp_xrp_b1.configure(background="green",text="sincronizado")
        else:
            self.bitstamp_xrp_b1.configure(background="red",text="desactualizado")

    def _get_db_state_bnnc_btcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando binance btcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("bnnc","btcusd")
        db._close()
        self.binance_btc_e1.delete(0, tk.END)
        self.binance_btc_e1.insert(0, str(time_min))
        self.binance_btc_e3.delete(0, tk.END)
        self.binance_btc_e3.insert(0, str(time_max))
        self.binance_btc_e2.delete(0, tk.END)
        self.binance_btc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.binance_btc_e4.delete(0, tk.END)
        self.binance_btc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.binance_btc_e5.delete(0, tk.END)
        self.binance_btc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.binance_btc_b1.configure(background="green",text="sincronizado")
        else:
            self.binance_btc_b1.configure(background="red",text="desactualizado")

    def _get_db_state_bnnc_ethusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando binance ethusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("bnnc","ethusd")
        db._close()
        self.binance_eth_e1.delete(0, tk.END)
        self.binance_eth_e1.insert(0, str(time_min))
        self.binance_eth_e3.delete(0, tk.END)
        self.binance_eth_e3.insert(0, str(time_max))
        self.binance_eth_e2.delete(0, tk.END)
        self.binance_eth_e2.insert(0, datetime.fromtimestamp(time_min))
        self.binance_eth_e4.delete(0, tk.END)
        self.binance_eth_e4.insert(0, datetime.fromtimestamp(time_max))
        self.binance_eth_e5.delete(0, tk.END)
        self.binance_eth_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.binance_eth_b1.configure(background="green",text="sincronizado")
        else:
            self.binance_eth_b1.configure(background="red",text="desactualizado")

    def _get_db_state_bnnc_ltcusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando binance ltcusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("bnnc","ltcusd")
        db._close()
        self.binance_ltc_e1.delete(0, tk.END)
        self.binance_ltc_e1.insert(0, str(time_min))
        self.binance_ltc_e3.delete(0, tk.END)
        self.binance_ltc_e3.insert(0, str(time_max))
        self.binance_ltc_e2.delete(0, tk.END)
        self.binance_ltc_e2.insert(0, datetime.fromtimestamp(time_min))
        self.binance_ltc_e4.delete(0, tk.END)
        self.binance_ltc_e4.insert(0, datetime.fromtimestamp(time_max))
        self.binance_ltc_e5.delete(0, tk.END)
        self.binance_ltc_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.binance_ltc_b1.configure(background="green",text="sincronizado")
        else:
            self.binance_ltc_b1.configure(background="red",text="desactualizado")

    def _get_db_state_bnnc_xrpusd(self):
        self.text.insert(tk.END,"\n[msg] - recuperando binance xrpusd de la BD")
        db = DbHandler()
        time_min,time_max,count = db._get_db_state("bnnc","xrpusd")
        db._close()
        self.binance_xrp_e1.delete(0, tk.END)
        self.binance_xrp_e1.insert(0, str(time_min))
        self.binance_xrp_e3.delete(0, tk.END)
        self.binance_xrp_e3.insert(0, str(time_max))
        self.binance_xrp_e2.delete(0, tk.END)
        self.binance_xrp_e2.insert(0, datetime.fromtimestamp(time_min))
        self.binance_xrp_e4.delete(0, tk.END)
        self.binance_xrp_e4.insert(0, datetime.fromtimestamp(time_max))
        self.binance_xrp_e5.delete(0, tk.END)
        self.binance_xrp_e5.insert(0, str(count))
        if abs(float(self.timestamp_local.get())-time_max)<3600:
            self.binance_xrp_b1.configure(background="green",text="sincronizado")
        else:
            self.binance_xrp_b1.configure(background="red",text="desactualizado")

    def _fetch_data(self):
        # comprobar si la hora esta bien
        if self.timestamp_bupdate['background']=="grey":
            self._get_server_timestamp()
            self.text.insert(tk.END, "\n[msg] - recuperando la hora de Kraken")
        elif not self.timestamp_bupdate['background']=="green":
            self.text.insert(tk.END,"\n[err] - problema recuperando la hora de Kraken")
            exit()
       
        fd = FetchData()
        dh = DbHandler()

        for i in range(1,10):

            ## Kraken
            # comprobar si btcusd no esta en verde
            if self.kraken_btc_b1['background']=="grey":
                #print("Boton Kraken BTCUSD en gris")
                self._get_db_state_krkn_btcusd()
            elif not self.kraken_btc_b1['background']=="green":
                #print("Boton Kraken BTCUSD ni gris ni en verde")
                df = fd._fetch_krkn("btcusd","XXBTZUSD")
                dh._insert_df('krkn','btcusd',df)
            self._get_db_state_krkn_btcusd()

            if self.kraken_eth_b1['background']=="grey":
                self._get_db_state_krkn_ethusd()
            elif not self.kraken_eth_b1['background']=="green":
                df = fd._fetch_krkn("ethusd","XETHZUSD")
                dh._insert_df('krkn','ethusd',df)
            self._get_db_state_krkn_ethusd()
        
            if self.kraken_ltc_b1['background']=="grey":
                self._get_db_state_krkn_ltcusd()
            elif not self.kraken_ltc_b1['background']=="green":
                df = fd._fetch_krkn("ltcusd","XLTCZUSD")
                dh._insert_df('krkn','ltcusd',df)
            self._get_db_state_krkn_ltcusd()

            ## Bitfinex
            if self.bitfinex_btc_b1['background']=="grey":
                self._get_db_state_btfn_btcusd()
            elif not self.bitfinex_btc_b1['background']=="green":
                df = fd._fetch_btfn("btcusd","tBTCUSD")
                dh._insert_df('btfn','btcusd',df)
            self._get_db_state_btfn_btcusd()

            if self.bitfinex_eth_b1['background']=="grey":
                self._get_db_state_btfn_ethusd()
            elif not self.bitfinex_eth_b1['background']=="green":
                df = fd._fetch_btfn("ethusd","tETHUSD")
                dh._insert_df('btfn','ethusd',df)
            self._get_db_state_btfn_ethusd()
        
            if self.bitfinex_ltc_b1['background']=="grey":
                self._get_db_state_btfn_ltcusd()
            elif not self.bitfinex_ltc_b1['background']=="green":
                df = fd._fetch_btfn("ltcusd","tLTCUSD")
                dh._insert_df('btfn','ltcusd',df)
            self._get_db_state_btfn_ltcusd()

            ## Bitstamp
            #if self.bitstamp_btc_b1['background']=="grey":
            #    self._get_db_state_btst_btcusd()
            #elif not self.bitstamp_btc_b1['background']=="green":
            #    df = fd._fetch_btst("btcusd","XXBTZUSD")
            #    dh._insert_df('btst','btcusd',df)
            #self._get_db_state_btst_btcusd()

            #if self.bitstamp_eth_b1['background']=="grey":
            #    self._get_db_state_btst_ethusd()
            #elif not self.bitstamp_eth_b1['background']=="green":
            #    df = fd._fetch_btst("ethusd","XETHZUSD")
            #    dh._insert_df('btst','ethusd',df)
            #self._get_db_state_btst_ethusd()
        
            #if self.bitstamp_ltc_b1['background']=="grey":
            #    self._get_db_state_btst_ltcusd()
            #elif not self.bitstamp_ltc_b1['background']=="green":
            #    df = fd._fetch_btst("ltcusd","XLTCZUSD")
            #    dh._insert_df('btst','ltcusd',df)
            #self._get_db_state_btst_ltcusd()
        
            ## Coinbase
            #if self.coinbase_btc_b1['background']=="grey":
            #    self._get_db_state_cnbs_btcusd()
            #elif not self.coinbase_btc_b1['background']=="green":
            #    df = fd._fetch_cnbs("btcusd","XXBTZUSD")
            #    dh._insert_df('cnbs','btcusd',df)
            #self._get_db_state_cnbs_btcusd()

            #if self.coinbase_eth_b1['background']=="grey":
            #    self._get_db_state_cnbs_ethusd()
            #elif not self.coinbase_eth_b1['background']=="green":
            #    df = fd._fetch_cnbs("ethusd","XETHZUSD")
            #    dh._insert_df('cnbs','ethusd',df)
            #self._get_db_state_cnbs_ethusd()
        
            #if self.coinbase_ltc_b1['background']=="grey":
            #    self._get_db_state_cnbs_ltcusd()
            #elif not self.coinbase_ltc_b1['background']=="green":
            #    df = fd._fetch_cnbs("ltcusd","XLTCZUSD")
            #    dh._insert_df('cnbs','ltcusd',df)
            #self._get_db_state_cnbs_ltcusd()

            dh._fix_gaps()

            sleep(20)

def main():
    print("begin")
    main_window = tk.Tk()
    app = Application(main_window)
    app.mainloop()
    print("end")

if __name__ == '__main__':
    main()
