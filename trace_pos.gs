'reinit'
*constant
*main process
*zonal mean
*'open ./TP.'ex_type'.wave.ex.ctl'
'open ../../../bs/ncep/ncep.clim.y58-97.t42.ctl'

'set lev 400'
'set xlopts 1 5 0.15'
'set ylopts 1 5 0.15'
'set xlint 30'
'set ylint 10'
'set font 4'
'set time apr1958'

'define uspr = ave(u,t-1,t+1,1)'
'define vspr = ave(v,t-1,t+1,1)'



