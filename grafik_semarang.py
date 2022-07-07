import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

#sesuaikan tahun dan bulan
tahun = '2022'
bulan = '12'

list_bulan = {'01':'Januari','02':'Februari','03':'Maret','04':'April','05':'Mei','06':'Juni','07':'Juli','08':'Agustus','09':'September','10':'Oktober','11':'November','12':'Desember'}
list_sheet = {'01':'JAN','02':'FEB','03':'MAR','04':'APR','05':'MEI','06':'JUN','07':'JUL','08':'AGS','09':'SEPT','10':'OKT','11':'NOV','12':'DES'}
list_bln = {'01':31,'02':28,'03':31,'04':30,'05':31,'06':30,'07':31,'08':31,'09':30,'10':31,'11':30,'12':31}
list_dir = {'01':'1.JANUARI','02':'2.FEBRUARI','03':'3.MARET','04':'4.APRIL','05':'5.MEI','06':'6.JUNI','07':'7.JULI','08':'8.AGUSTUS','09':'9.SEPTEMBER','10':'10.OKTOBER','11':'11.NOVEMBER','12':'12.DESEMBER'}
list_tanggal = ['%.2d' % i for i in range(1,list_bln.get(bulan)+1)]

#Baca tabel pasut excel, pastikan tabel sesuai template tahun sebelumnya, sesuaikan dengan lokasi file nya
data  = pd.read_excel('E:/GRAFIK PASUT SEMARANG 2022/MASTER GRAFIK PASUT 2022 SMG PUSHIDROSAL.xls', 
    sheet_name=list_sheet.get(bulan),skiprows=6,skipfooter=4, header=None, usecols='B:Y')
im = plt.imread('E:/Logo-BMKG-new.png') #Baca logo BMKG

bln = np.arange(list_bln.get(bulan)+1)
for tanggal,tgl in zip(list_tanggal,bln):
    #Atur lokasi grafik disimpan
    dir_hasil = 'E:/GRAFIK PASUT SEMARANG 2022/{0}/'.format(list_dir.get(bulan))
    if not os.path.exists(dir_hasil):
        os.makedirs(dir_hasil)
    msl = np.full((24,),0.6)
    y = data.iloc[tgl,:]
    x = np.arange(1,25)
    y_tick = [0.0,0.2,0.4,0.6,0.8,1.0,1.2]
    fig, ax = plt.subplots(1,figsize=(10,6))
    plt.subplots_adjust(top=0.835,bottom=0.13,left=0.1,right=0.95,hspace=0.2,wspace=0.2)

    grph = ax.bar(x,y,color='steelblue',width=0.4,tick_label=x)
    ax.plot(x,msl,color='red',label='MSL',linewidth=2.5)
    ax.set_ylim(0,1.2)
    ax.set_xlim(0,25)
    ax.tick_params(axis='both', labelsize=12)
    ax.set_yticks(y_tick)
    ax.set_yticklabels(y_tick)
    ax.set_title('STASIUN METEOROLOGI MARITIM TANJUNG EMAS SEMARANG\nPRAKIRAAN PASANG SURUT HARIAN SEMARANG\nTanggal {0} {1} {2}'.format(tanggal,list_bulan.get(bulan),tahun),
    fontweight='bold',fontsize=14,pad=20)
    ax.bar_label(grph, label_type='edge',fontsize=12)
    ax.set_xlabel('Jam (WIB)',fontweight='bold',fontsize=12)
    ax.set_ylabel('Tinggi (meter)',fontweight='bold',fontsize=12)
    ax.grid(axis='y',color='dimgray')
    ax.set_facecolor('gainsboro')
    ax.legend(loc='upper right',fontsize=12)
    ax.text(0.85, -0.15, 'Sumber: PUSHIDROS TNI AL',fontsize=10,fontstyle='italic',
            horizontalalignment='center',
            verticalalignment='bottom',
            transform=ax.transAxes)
    
    #atur posisi logo BMKG
    newax = fig.add_axes([0.1, 0.845, 0.148, 0.148], anchor='NW', zorder=-1)
    newax.imshow(im)
    newax.axis('off')

    #simpan grafik
    plt.savefig('{0}/{1} {2} {3}'.format(dir_hasil,tanggal,list_bulan.get(bulan),tahun),dpi=200)
    print('plot tanggal {0} {1} selesai'.format(tanggal,list_bulan.get(bulan)))

    # plt.show()