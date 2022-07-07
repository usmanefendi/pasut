import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel('E:/Python/pasut/FEB2021.xlsx')
# awl = data['pasut']
# awl_tgl = data['waktu']

##transpose tabel
df = data.stack().reset_index()
tgl = pd.date_range(start='2022-05-01 00:00:00', end='2022-05-31 23:00:00',freq='H')
df['waktu'] = tgl
index = pd.to_datetime(df['waktu'])
df.index = index
df['waterlevel'] = df[0]


# plt.plot(df.index,df.waterlevel)
# plt.show()

df["anomaly"] = df['waterlevel'] - df['waterlevel'].mean()
print(df.head())
print('msl: ',df['waterlevel'].mean())
print('pasut maks: ',df.anomaly.max())
writer = pd.ExcelWriter('E:/Python/pasut/pushidros_2022_05.xlsx')
df["anomaly"].to_excel(writer,'Sheet1', header = True)
writer.save()





#buat ngisi kekosongan data
# tgl = pd.date_range(start='2020-10-15', end='2020-10-16',freq='10min')
# waterlevel = np.empty((int(len(tgl))))
# waterlevel[:] = np.nan

# for i in range(len(tgl)):
#     for j in range(len(awl_tgl)):
#         if str(tgl[i])[0:16] == str(awl_tgl[j])[0:16]:
#             waterlevel[i] = awl[j]


# data = {'waktu':tgl,'waterlevel':waterlevel}

# title = ['waktu','waterlevel']
# df = pd.DataFrame(data, columns = title)
# writer = pd.ExcelWriter('E:/python/pasut/pasut_1th/data_pasut_koreksi.xlsx')
# df.to_excel(writer,'Sheet1', header = True)
# writer.save()