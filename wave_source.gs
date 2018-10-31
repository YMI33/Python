'reinit'
'open ../TP.wave.dyn.ctl'

'set lat 30'
'set lon 100'
*P'set lev 200'
'set xlopts 1 5 0.15'
'set ylopts 1 5 0.15'
'set xlint 30'
'set font 4'
'set t 1 29'

*P'define bsterm= tloop(aave(bsf,lon=120,lon=150,lat=35,lat=55)*1e12)'
*P'define bvterm= tloop(aave(bkv,lon=120,lon=150,lat=35,lat=55)*1e12)'
*P'define tenterm= tloop(aave(ten,lon=120,lon=150,lat=35,lat=55)*1e12)'


