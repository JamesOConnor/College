#Dates to julian
import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import gdal
import os
import subprocess
import numpy.ma as ma

def Bigfires(year, latitude, longitude, minlatmaxlat, minlonmaxlon, frp):

        direct='/home/ucfajoc/DATA/Thesis/%d_%s%s/'%(year,latitude,longitude)
        fname='/home/ucfajoc/DATA/Thesis/%d_%s%s/FRP_%s_AllPs.txt'%(year,latitude,longitude,frp)
        fname2='/home/ucfajoc/DATA/Thesis/%d_%s%s/FRP_%s_AllPs.npy'%(year,latitude,longitude,frp)
        print fname
        x=np.array(range(8,345,16))
        counts=0
        count=0
        ucount=0
        a='ls /home/ucfajoc/DATA/Thesis/%d_%s%s/MOD*'%(year,latitude,longitude)
        proc=subprocess.Popen([a],stdout=subprocess.PIPE,shell=True)
        (out, err)=proc.communicate()
        b = out.split('\n')[:-1]

        fires=np.loadtxt('/home/ucfajoc/DATA/Thesis/%d_%s%s/Fires_%d%s%s.csv'%(year,latitude,
longitude,year,latitude,
longitude),dtype=float,delimiter=',',skiprows=1,usecols=(0,1,11))
        full=np.loadtxt('/home/ucfajoc/DATA/Thesis/%d_%s%s/Fires_%d%s%s.csv'%(year,latitude,
longitude, year,latitude, longitude), delimiter=",", dtype=str)
#bigfires=np.where(fires[:,2]>1000)[0]
#spainfires=np.where(fires[bigfires,0]>35)[0]

        if longitude[4]=='W':
                l=(fires[:,0]>int(minlatmaxlat[0:3])/10) &
(fires[:,0]<int(minlatmaxlat[4:7])/10) &
(fires[:,1]>-int(minlonmaxlon[0:4])/10) &
(fires[:,1]<-int(minlonmaxlon[5:9])/10) & (fires[:,2]>frp)
                lt=np.where(l==True)[0]
                bigfires=fires[lt]
        else:
                l=(fires[:,0]>int(minlatmaxlat[0:3])/10) &
(fires[:,0]<int(minlatmaxlat[4:7])/10) &
(fires[:,1]>int(minlonmaxlon[0:4])/10) &
(fires[:,1]<int(minlonmaxlon[5:9])/10) & (fires[:,2]>frp)
                lt=np.where(l==True)[0]
                bigfires=fires[lt]

        p=fires[lt]
        print p
        pixels=np.zeros_like(p)
        print pixels.shape

        if latitude[3]=='N':
                for i in xrange(len(p[:,0])):
                        pixels[i,0]=8000-int((p[i,0]*100))
                        pixels[i,1]=int((np.absolute(p[i,1]))*100-longitude[0:4])
        elif latitude[3]=='S':
                for i in xrange(len(p[:,0])):
                            pixels[i,0]=4500-int((p[i,0]*100))
                            pixels[i,1]=int(p[i,1]*100)-int(longitude[0:4])*10
        print pixels

###Generate data

        if os.path.exists(fname)==False:
                for i in xrange(len(p[:,0])):
                        for y in xrange(7):
                                j = 'gdallocationinfo -valonly -wgs84 %d_%s%s/param_%d_%d_%s%s.vrt
%f %f >> %d_%s%s/FRP_%s_AllPs.txt'%(year,latitude,longitude,y,year,
latitude,longitude,p[i,1],p[i,0],year,latitude,longitude,frp)
                                os.system(j)
                data=np.loadtxt('/home/ucfajoc/DATA/Thesis/%d_%s%s/FRP_%s_AllPs.txt'%(year,latitude,
longitude,frp))
        else: data=np.loadtxt('/home/ucfajoc/DATA/Thesis/%d_%s%s/FRP_%s_AllPs.txt'%(year,latitude,
longitude,frp))
#####

        dates=full[lt+1][:,5]

        k=np.zeros((len(dates),len(b),7))

        for n,i in enumerate(data):
                k[n/154, n%22,(n/22)%7]=i
        k=ma.masked_greater(k,65534)
        k=ma.masked_less(k,0)


        font = {'family' : 'normal',
                'weight' : 'bold',
                 'size'   : 6}

        matplotlib.rc('font', **font)

        #dates to julian
        fmt = '%Y-%m-%d'
        julian=np.zeros_like(dates).astype(int)
        for i,date in enumerate(dates):
                julian[i]=datetime.datetime.strptime(date,fmt).timetuple().tm_yday

        ooo=np.zeros((len(p[:,0]),len(b),7))

        xlocs=pixels[:,1].astype(int)
        ylocs=pixels[:,0].astype(int)

        if os.path.exists(fname2)==False:
                for counter,file in enumerate(b):
                        print counter
                        g=gdal.Open('HDF4_SDS:UNKNOWN:'+file+':14')
                        ooo[:,counter,:]=g.ReadAsArray()[:,ylocs,xlocs].T
                np.save(direct+'FRP_%s_AllPs'%(frp),ooo)
        else:ooo=np.load(direct+'FRP_%s_AllPs.npy'%(frp))

        if os.path.exists(direct+'Fireplots_%s'%(frp))==False:
                hh='mkdir %sFireplots_frp%s'%(direct,frp)
                os.system(hh)
#ooo=np.load('UNCarray.npy')
#ooo=ma.masked_greater(ooo,65534)
#ooo=ma.masked_less(ooo,0)

        for go in xrange(len(bigfires)):

            y1=ma.masked_less((k[go,:,0]-500)*.002,0)
            print ma.count(y1),np.max(y1)
            y2=(k[go,:,1]-10000)*.0001
            y3=(k[go,:,2]-10000)*.0001
            y4=(k[go,:,3]-10000)*.0001
            y5=(k[go,:,4]-10000)*.0001
            y6=(k[go,:,5]-10000)*.0001
            y7=(k[go,:,6]-10000)*.0001

            unc1=ma.masked_less(ooo[go,:,0]*.0002,0.05)
            unc2=ma.masked_less(ooo[go,:,1]*.0002,0.05)
            unc3=ma.masked_less(ooo[go,:,2]*.0002,0.05)
            unc4=ma.masked_less(ooo[go,:,3]*.0002,0)
            unc5=ma.masked_less(ooo[go,:,4]*.0002,0.05)
            unc6=ma.masked_less(ooo[go,:,5]*.0002,0.05)
            unc7=ma.masked_less(ooo[go,:,6]*.0002,0)

            ax1=plt.subplot(421)
            ax1.plot(x, y1, 'ko',ms=2)
            ax1.errorbar(x, y1,yerr=unc1, fmt='ko',ms=2)
            ax1.set_ylim([0,3.5])
            plt.axvline(x=julian[go],color='r')
            ax1.yaxis.set_ticks(np.arange(0, 3.5, .5))
            t=plt.title('Effective Leaf Area Index')
            t.set_position((.5,1.07))

            ax2=plt.subplot(422)
            ax2.plot(x, y2, 'ko',ms=2)
            ax2.errorbar(x, y2,yerr=unc2, fmt='ko',ms=2)
            plt.axvline(x=julian[go],color='r')
            i=np.around((np.max(y2)-np.min(y2)),3)*2
            ax2.yaxis.set_ticks(np.arange(0, .3, .05))
            ax2.set_ylim([0,.3])
            t=plt.title('Effective Single Scattering Albedo (VIS)')
            t.set_position((.5,1.07))

            ax3=plt.subplot(423)
            ax3.plot(x, y3, 'ko',ms=2)
            ax3.errorbar(x, y3,yerr=unc3, fmt='ko',ms=2)
            plt.axvline(x=julian[go],color='r')
            i=np.around((np.max(y3)-np.min(y3)),3)/5
            ax3.yaxis.set_ticks(np.arange(0, 1.6, .4))
            t=plt.title('Effective preferred direction of scattering by the
vegetation layer (VIS)')
            t.set_position((.5,1.07))
            ax3.set_ylim([0,1.6])

            ax4=plt.subplot(424)
            ax4.plot(x, y4, 'ko',ms=2)
            ax4.errorbar(x, y4,yerr=unc4, fmt='ko',ms=2)
            plt.axvline(x=julian[go],color='r')
            i=np.around((np.max(y4)-np.min(y4)),3)/5
            ax4.yaxis.set_ticks(np.arange(0, .7, .05))
            ax4.set_ylim([0,.25])
            t=plt.title('True Background Albedo (VIS)')
            t.set_position((.5,1.07))

            ax5=plt.subplot(425)
            ax5.plot(x, y5, 'ko',ms=2)
            ax5.errorbar(x, y5,yerr=unc5, fmt='ko',ms=2)
            plt.axvline(x=julian[go],color='r')
            i=np.around((np.max(y5)-np.min(y5)),3)/5
            ax5.yaxis.set_ticks(np.arange(0, 1, .2))
            ax5.set_ylim([0,1])
            t=plt.title('Effective Single Scattering Albedo (NIR)')
            t.set_position((.5,1.07))

            ax6=plt.subplot(426)
            ax6.plot(x, y6, 'ko',ms=2)
            ax6.errorbar(x, y6,yerr=unc6, fmt='ko',ms=2)
            plt.axvline(x=julian[go],color='r')
            i=np.around((np.max(y6)-np.min(y6)),3)/5
            ax6.yaxis.set_ticks(np.arange(0, 1, 1))
            t=plt.title('Effective preferred direction of scattering by the
vegetation layer (NIR)')
            t.set_position((.5,1.07))
            ax6.set_ylim([0,4])

            ax7=plt.subplot(427)
            ax7.plot(x, y7, 'ko',ms=2)
            ax7.errorbar(x, y7,yerr=unc7, fmt='ko',ms=2)
            plt.axvline(x=julian[go],color='r')
            ax7.set_ylim([0,.45])
            ax7.yaxis.set_ticks(np.arange(0,.5 ,.1))
            t=plt.title('True Background Albedo (NIR)')
            t.set_position((.5,1.07))

            ax1.set_xlim([0,350])
            ax2.set_xlim([0,350])
            ax3.set_xlim([0,350])
            ax4.set_xlim([0,350])
            ax5.set_xlim([0,350])
            ax6.set_xlim([0,350])
            ax7.set_xlim([0,350])

            plt.subplots_adjust(hspace=.5)
            plt.savefig('/home/ucfajoc/DATA/Thesis/%d_%s%s/Fireplots_frp%s/%s_%s_frp%s_lat%s_lon%s.jpg'%(year,latitude,longitude,frp,
go,dates[go],p[go,2],p[go,0],p[go,1]))
            plt.clf()
