import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import utide
from datetime import datetime

data = pd.read_excel("E:/python/pasut/base_data/base_2018_combine.xlsx") 

index = pd.to_datetime(data['waktu'])

data.index = index
# # print(data.index)
# # data.loc[data['waterlevel'] < 0.8, 'waterlevel'] = np.nan
# # data.loc[data['waterlevel'] > 2.2, 'waterlevel'] = np.nan
# data["anomaly"] = data["waterlevel"] - data["waterlevel"].mean()
data["anomaly"] = data["anomaly"].interpolate()
# plt.plot(data.index,data.anomaly)
# plt.grid(True)
# plt.title('Data Pasut Januari 2018 - Mei 2022')
# plt.show()

coef = utide.solve(
    data.index,
    data["anomaly"],
    lat=-6.94773,
    method="ols",
    conf_int="MC",
    verbose=True,
)
# print(coef.keys())

#membuat prediksi
t_prediksi = pd.date_range(start='2022-05-01 00:00:00', end='2022-05-31 23:00:00',freq='H')
# t_prediksi = pd.date_range(start='2022-11-30 18:00:00', end='2022-12-31 17:00:00',freq='H')
tide = utide.reconstruct(t_prediksi, coef, verbose=True)
# waterlevel = (tide.h) * 100
# pasut = np.round((waterlevel + 130))

# tahun = np.repeat(2022, 31*24)
# bulan = np.repeat(12, 31*24)
# tgl = np.repeat(np.array([i for i in range(1,32)]), 24)
# jam_WIB = np.tile(np.array([j for j in range(1,25)]),31)

# data = {'Time (UTC)':t_prediksi,'tahun':tahun,'bulan':bulan,'Tanggal':tgl,'Jam (WIB)':jam_WIB,'Pasut (cm)':pasut,'waterlevel':waterlevel}
# title = ['Time (UTC)','tahun','bulan','Tanggal','Jam (WIB)','Pasut (cm)','waterlevel']
# df = pd.DataFrame(data, columns = title)
# writer = pd.ExcelWriter('E:/python/pasut/Prakiraan Pasut BMKG/12.Desember2022.xlsx')
# df.to_excel(writer,'Sheet1', header = True)
# writer.save()





##plot hasil prediksi
obs = pd.read_excel('E:/python\pasut/base_data/2022-05_AWS2.xlsx')
pushidros = pd.read_excel('E:/python/pasut/pushidros_2022_05.xlsx')
corr_BMKG = round(np.corrcoef(obs.anomaly,tide.h)[1,0],2)
corr_pushidros = round(np.corrcoef(obs.anomaly,pushidros.anomaly)[1,0],2)
rmse_bmkg = round(np.linalg.norm(tide.h - obs.anomaly) / np.sqrt(len(t_prediksi)),2)
rmse_pushidros = round(np.linalg.norm(pushidros.anomaly - obs.anomaly) / np.sqrt(len(t_prediksi)),2)

fig, (ax0, ax1) = plt.subplots(figsize=(10, 5), nrows=2, sharex=True)
plt.subplots_adjust(left=0.10, right=0.975, hspace=0.1)
ax0.plot(t_prediksi, obs.anomaly, label="Observasi Manual", color="black",linewidth=1.0)
ax0.plot(t_prediksi, tide.h, label="Prediksi BMKG", linestyle='solid',color="red",linewidth=0.6)
ax0.set_ylim(-0.8,0.8)
ax0.set_ylabel('Elevasi (m)', fontsize=11)
ax0.legend(loc='upper right')
ax0.text(0.01, 0.05, 'Korelasi: {0}\nRMSE: {1}'.format(corr_BMKG,rmse_bmkg), horizontalalignment='left',transform=ax0.transAxes, fontsize=9)

ax1.plot(t_prediksi,obs.anomaly, label="Observasi Manual", color="black",linewidth=1.0)
ax1.plot(t_prediksi, pushidros.anomaly, label="Prediksi Pushidros", linestyle='solid',color="blue",linewidth=0.6)
ax1.set_ylim(-0.8,0.8)
ax1.set_ylabel('Elevasi (m)', fontsize=11)
ax1.legend(loc='upper right')
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
ax1.text(0.01, 0.05, 'Korelasi: {0}\nRMSE: {1}'.format(corr_pushidros,rmse_pushidros), horizontalalignment='left',transform=ax1.transAxes, fontsize=9)
ax1.set_xlabel('Tanggal', fontsize=11)
ax0.title.set_text('Perbandingan Prediksi Pasut BMKG & Pushidrosal terhadap data Observasi Manual Mei 2022')
plt.show()


