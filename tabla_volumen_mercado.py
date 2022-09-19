#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np


labels = ['Kraken', 'Bitfinex', 'Binance', 'Bitstamp']
btc_volume = [85711, 144795, 1154492, 79656]
eth_volume = [67341, 77078, 772211, 43512]
ltc_volume = [5597, 7612, 88544, 5253]
xrp_volume = [8028, 13961, 255240, 18655]

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

print(x)

fig, ax = plt.subplots()
rects1 = ax.bar(x - width*1.5, btc_volume, width, label='btc')
rects2 = ax.bar(x - width/2, eth_volume, width, label='eth')
rects3 = ax.bar(x + width/2, ltc_volume, width, label='ltc')
rects4 = ax.bar(x + width*1.5, xrp_volume, width, label='xrp')


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Volumen de mercado 2021 (millones de $)')
ax.set_title('Total agrupado por casa de cambio y criptomoneda')
ax.set_xticks(x, labels)
ax.legend()

ax.bar_label(rects1, fmt='%d', padding=2, rotation=45)
ax.bar_label(rects2, fmt='%d', padding=2, rotation=45)
ax.bar_label(rects3, fmt='%d', padding=2, rotation=45)
ax.bar_label(rects4, fmt='%d', padding=2, rotation=45)

fig.tight_layout()
plt.ylim(0, 1300000)
plt.ticklabel_format(style='plain', axis="y")
plt.show()