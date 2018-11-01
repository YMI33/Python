# this script is used for showing how the 
# tracer is moved by wind on the sphere surface

#import lib
import numpy as np
from numpy import deg2rad, rad2deg, sin, cos, tan, arcsin, arctan2
from gsscript import gsscript
from scipy.interpolate import Rbf
from matplotlib import pyplot as plt
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

#get uwnd and vwnd
gs = gsscript("./trace_pos.gs")
print(gs.ga)
gs.ga('open ../TP.wave.dyn.ctl')
u    = gs.ga.exp("uspr") 
v    = gs.ga.exp("vspr")
lat  = gs.ga.exp("lat")
lon  = gs.ga.exp("lon")
#vara = "bsf.2(t=" + str(dyend) +")"
vort = gs.ga.exp("bsf.2(t=10)")
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

