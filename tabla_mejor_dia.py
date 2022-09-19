import numpy as np
import matplotlib
import matplotlib.pyplot as plt

horas = ["domingo","lunes","martes","miercoles","jueves","viernes","sabado"]
divisas = ["krkr btc", "krkr eth", "krkr ltc", "krkr xrp", "btfn btc", "btfn eth", "btfn ltc", "btfn xrp"]

# harvest = np.array([[0.1825,0.8779,-0.3336,1.2195,0.1779,0.8704,-0.2892,1.3884],
#                 [-0.1234,-1.1265,-0.1539,-0.3622,-0.1254,-1.1284,-0.1229,-0.2342],
#                 [-0.5288,-1.0148,-0.4505,-0.9852,-0.5172,-1.0063,-0.3728,-0.8164],
#                 [-0.1051,-0.1917,0.318,-0.6731,-0.1007,-0.1886,0.3397,-0.5846],
#                 [0.1427,0.6765,0.2277,-0.0501,0.132,0.663,0.2504,0.0704],
#                 [-0.0114,0.1196,-0.2478,-0.5776,-0.0208,0.1019,-0.2212,-0.4054],
#                 [0.4726,0.7333,0.2457,0.4937,0.4623,0.7177,0.2824,0.5651]])

harvest = np.array([[0.6855,1.2796,1.0242,0.2894,0.689,1.2811,0.9814,0.3919],
                    [-1.6821,-1.5447,-1.1403,0.1464,-1.6728,-1.5504,-1.1877,0.1661],
                    [-0.6079,-0.7162,-0.3115,0.5515,-0.6189,-0.7435,-0.3573,0.5662],
                    [0.0394,-0.4345,-0.2997,-0.3214,0.0315,-0.4665,-0.3934,-0.2756],
                    [0.4795,-0.2404,-0.7341,-0.9955,0.4715,-0.2575,-0.7835,-0.9421],
                    [0.4482,0.2395,-0.1845,-0.5143,0.439,0.2097,-0.2483,-0.4798],
                    [0.6593,1.1242,1.088,0.1302,0.6454,1.0689,0.9772,0.1678]])

fig, ax = plt.subplots()
im = ax.imshow(harvest)

# Show all ticks and label them with the respective list entries
ax.set_xticks(np.arange(len(divisas)), labels=divisas)
ax.set_yticks(np.arange(len(horas)), labels=horas)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(len(horas)):
    for j in range(len(divisas)):
        text = ax.text(j, i, harvest[i, j], ha="center", va="center", color="w")

ax.set_title("Mejor y peor hora del día 2020")
fig.tight_layout()
plt.show()