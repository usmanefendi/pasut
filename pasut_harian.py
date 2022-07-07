import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import utide
from datetime import datetime

data = pd.read_excel("E:/python/pasut/2021/2.Feb2021.xlsx") 

index = pd.to_datetime(data['waktu'])

data.index = index
# print(data.index)
# data.loc[data['waterlevel'] < 0.8, 'waterlevel'] = np.nan
# data.loc[data['waterlevel'] > 2.2, 'waterlevel'] = np.nan
data["anomaly"] = data["waterlevel"] - data["waterlevel"].mean()
data["anomaly"] = data["anomaly"].interpolate()
# plt.plot(data.index,data.waterlevel)
# plt.grid(True)
# plt.show()

coef = utide.solve(
    data.index,
    data["anomaly"],
    lat=-6.94773,
    method="ols",
    conf_int="MC",
    verbose=False,
)
print(coef.keys())

tide = utide.reconstruct(data.index, coef, verbose=False)
print(tide.keys())
# t = data.index.to_pydatetime()
t = data.index
tgl = pd.date_range(start='2021-02-01 07:00:00', end='2021-03-01 06:00:00',freq='H')

fig, (ax0, ax1) = plt.subplots(figsize=(10, 5), nrows=2, sharex=True)
plt.subplots_adjust(left=0.10, right=0.975, hspace=0.1)
ax0.plot(tgl[113:139], data.anomaly[113:139], label="Observasi", color="black",linewidth=1.0)
ax0.plot(tgl[113:139], tide.h[113:139], label="Pasut Astronomis", linestyle='solid',color="red",linewidth=0.6)
# ax0.tick_params(which='major',length=6, labelsize=10, labelcolor='black')
ax0.set_ylim(-1,1)
ax0.set_ylabel('Elevasi (m)', fontsize=11)
# ax0.axvline(datetime(2021,2,11),color='blue', label='bulan baru',ls='--')
# # ax0.axvline(datetime(2022,4,30),color='blue',ls='--')
# ax0.axvline(datetime(2021,2,3),color='green', label='perigee',ls='--')
# # ax0.axvline(datetime(2022,1,30),color='green',ls='--')
# ax0.axvline(datetime(2021,2,27),color='red', label='purnama',ls='--')
ax0.grid(True,ls=':')
ax0.title.set_text('6 Februari 2021')
residu = data.anomaly - tide.h

ax1.plot(tgl[113:139], residu[113:139], color="C2",linewidth=1.0)
ax1.set_ylim(-0.5,0.5)
# ax1.tick_params(which='major',length=6,labelsize=10, labelcolor='black')
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
# ax1.xaxis.set_minor_locator(mdates.DayLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.set_ylabel('Residual (m)', fontsize=11)
ax1.set_xlabel('Jam (WIB)', fontsize=11)
ax1.grid(True,ls=':')
fig.autofmt_xdate()
fig.legend(ncol=5, loc="lower left",title_fontsize=10,bbox_to_anchor=(0.1, 0.2),framealpha=0.2)

# plt.savefig('E:/python/pasut/2021/6Feb2021.png',dpi=300)
plt.show()
