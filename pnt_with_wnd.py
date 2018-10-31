# this script is used for showing how the 
# tracer is moved by wind on the sphere surface

#import lib
import numpy as np
#from mpl_toolkits.basemap import Basemap
from numpy import deg2rad, rad2deg, sin, cos, tan, arcsin, arctan2
from gsscript import gsscript
from py3grads import Grads
from scipy.interpolate import Rbf
from matplotlib import pyplot as plt
ga    = Grads(verbose=False)
#user setting
tstp  = 1
dyend = 10 

#E_st = np.array(90)
#N_st = np.array(30)
E_st  = np.linspace( 80,120, 5)
N_st  = np.linspace( 25, 40, 5)

#constant
a     = 6.37e6
tintv = tstp  * 3600
pi    = 3.14159
spend = dyend * 86400 / tintv
#spend = 1
#main process
notes = []
#execute gs script
gsdic = {
        "note"   : "notes = notes + gs.state",
        "grads"  : "ga(gs.state)",
        "gs"     : "gs.state"
        }

for line in open("./trace_pos.gs"):
  if not line: 
      continue
  if line == "return":
      break
  gs = gsscript(line)
  exec(gsdic[gs.type])

#get uwnd and vwnd
ga('open ../TP.wave.dyn.ctl')
u    = ga.exp("uspr") 
v    = ga.exp("vspr")
lat  = ga.exp("lat")
lon  = ga.exp("lon")
#vara = "bsf.2(t=" + str(dyend) +")"
vara = "bsf.2(t=10)"
vort = ga.exp(vara)
print(vara)
#langrangian trace
lons,lats  = np.meshgrid( E_st, N_st )
lons       = lons.ravel()
lats       = lats.ravel()
trc        = np.full( [int(spend), 2, len(lons) ], np.nan )

#interpolate
intu = Rbf(lon,lat,u,function = "inverse")
intv = Rbf(lon,lat,v,function = "inverse")

#time advance
for t in range(int(spend)): 
 
 trc[t, : ,:]  = [lons,lats]
 pntu = intu(lons,lats)
 pntv = intv(lons,lats)

# Radian conversion
 lats = deg2rad(lats)
 lons = deg2rad(lons)

# Angle of movement trace - deta
# Angle for movement direction - theta
 deta = np.sqrt(pntu**2+pntv**2) * tintv / a
 theta= arctan2(pntu,pntv)

# Spherical law of cosines & sinines
 sinN = sin(lats) * cos(deta) + cos(lats) * sin(deta) * cos(theta)
 late = arcsin(sinN)
 lone = lons + arcsin( sin(theta) * sin(deta) / cos(late))
 
# Degree conversion
 late = rad2deg(late)
 lone = rad2deg(lone)

 lats = late
 lone[lone>=360] = lone[lone>=360] -360
 lons = lone

# plt.countourf(lon,lat,u)
#Basemap.drawcoastlines()
levels  = np.arange(-6e-12,6e-12,5e-13)
fig, ax = plt.subplots()
CS = ax.contourf(lon,lat,vort,levels,cmap="coolwarm")
plt.colorbar(CS)
plt.plot(trc[:,0], trc[:,1], color = "k", alpha = 0.1)
plt.show()

