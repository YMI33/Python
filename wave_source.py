#import lib
import numpy as np
#from mpl_toolkits.basemap import Basemap
from numpy import mean
from gsscript import gsscript
from py3grads import Grads
from scipy.interpolate import Rbf
from matplotlib import pyplot as plt
ga    = Grads(verbose=False)

lev_p = [200,500]
lon_r = [[75,105],[110,140],[150,180]]
lat_r = [[25,45],[35,55],[45,65]]
count = 5
notes = ""
bsf   = [None]*(count+1)
bkv   = [None]*(count+1)
ten   = [None]*(count+1)
psi   = [None]*(count+1)
subplot_title   = [None]*(count+1)

#execute gs script
gsdic = {
        "note"   : "notes= notes + gs.state",
        "grads"  : "ga(gs.state)",
        "gs"     : "gs.state"
        }

for line in open("./wave_source.gs"):
  if not line: 
      continue
  if line == "return":
      break
  gs = gsscript(line)
  exec(gsdic[gs.type])

#user setting env

flag_l = True
for l in range(count+1):
 k      = l % 3
 if flag_l: 
  ga("set lev " + str(lev_p[0]))
  subplot_title[l] = "Level " + str(lev_p[0])
 else:
  ga("set lev " + str(lev_p[1]))
  subplot_title[l] = "Level " + str(lev_p[1])
 subplot_title[l] = subplot_title[l] + ", Center " + str(mean(lon_r[k][:])) + "$^oE, "+ str(mean(lat_r[k][:])) + "^oN$"
 flag_l = not flag_l
 print(flag_l)
 print(subplot_title)
 #varable area average 
 gasta  = "define bsterm = tloop(aave(bsf,lon=" + str(lon_r[k][0]) + ",lon=" + str(lon_r[k][1]) + ",lat=" + str(lat_r[k][0]) + ",lat=" + str(lat_r[k][1]) + ")*1e12)"
 ga(gasta)
 gasta  = "define bvterm = tloop(aave(bkv,lon=" + str(lon_r[k][0]) + ",lon=" + str(lon_r[k][1]) + ",lat=" + str(lat_r[k][0]) + ",lat=" + str(lat_r[k][1]) + ")*1e12)"
 ga(gasta)
 gasta  = "define tenterm = tloop(aave(ten,lon=" + str(lon_r[k][0]) + ",lon=" + str(lon_r[k][1]) + ",lat=" + str(lat_r[k][0]) + ",lat=" + str(lat_r[k][1]) + ")*1e12)"
 ga(gasta)
 gasta  = "define psiterm = tloop(aave(psi,lon=" + str(lon_r[k][0]) + ",lon=" + str(lon_r[k][1]) + ",lat=" + str(lat_r[k][0]) + ",lat=" + str(lat_r[k][1]) + ")/1e5)"
 ga(gasta)
 #analysis term
 bsf[l]    = ga.exp("bsterm") 
 bkv[l]    = ga.exp("bvterm") 
 ten[l]    = ga.exp("tenterm") 
 psi[l]    = ga.exp("psiterm") 

for l in range(count+1):
 plt.subplot(2,3,l+1)
 plt.plot(np.arange(1.,30.,1.),bsf[l],'b')
 plt.plot(np.arange(1.,30.,1.),bkv[l],'r')
 plt.plot(np.arange(1.,30.,1.),ten[l],'k')
 plt.plot(np.arange(1.,30.,1.),psi[l],'k--')
 plt.legend(["basic flow term","basic vorticity term","tendency term","psi"],loc = "upper left")
 plt.title(subplot_title[l])

plt.show()
 
 
