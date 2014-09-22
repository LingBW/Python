# forecastmulti_track

'''
GENERAL NOTES:
1. Nkosi's version of Conner's multi_track; designed to forecast drifter movement. Comments and adjustments also made my JiM and Jian.
2. Initializations (HARDCODES) need to be at the beginning of the program or function
3. If any changes are made, the flowcharts MUST be updated
'''

#Import modules

import sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta
from matplotlib import path
import calendar
import pytz
sys.path.append('../bin')
import netCDF4
import track_functions
from track_functions import *

#initialize constants
drifter_ids = ['1474207011']
mod = 'GOM3' # mod has to be '30yr' or 'GOM3' or 'massbay'
filename='drift_noaa_morgan_2014_1.dat'
depth = -1
days = 3
#starttime = datetime(2014, 7, 22, 17,0,0,0,pytz.UTC)
starttime=None
for ID in drifter_ids:
    print ID
    if filename:
         drifter = get_drifter(ID,filename) # Retrive drifter data
    else:
         drifter = get_drifter(ID)
    if starttime:

         if days:
             nodes_drifter = drifter.get_track(starttime,days)

         else:
            nodes_drifter = drifter.get_track(starttime)
        
    else:
        nodes_drifter = drifter.get_track()
       
    ''' determine latitude, longitude, start, and end times of the drifter?'''

    #lon, lat = nodes_drifter['lon'][0], nodes_drifter['lat'][0]
    lon, lat = nodes_drifter['lon'][-1], nodes_drifter['lat'][-1]
    # adjust for the added 5 hours in the models
    starttime = nodes_drifter['time'][-1]#-timedelta(hours=5)
    endtime = nodes_drifter['time'][-1]+timedelta(days=1)
    print starttime

    ''' read data points from fvcom and roms websites and store them'''
    get_fvcom_obj = get_fvcom(mod)
    url_fvcom = get_fvcom_obj.get_url(starttime, endtime)
    nodes_fvcom = get_fvcom_obj.get_track(lon,lat,depth,url_fvcom) # iterates fvcom's data
    #get_roms_obj = get_roms()
    #url_roms = get_roms_obj.get_url(starttime, endtime)
    #nodes_roms = get_roms_obj.get_track(lon, lat, depth, url_roms)
    
    #if type(nodes_roms['lat']) == np.float64: # ensures that the single point case still functions properly
    
      # nodes_roms['lon'] = [nodes_roms['lon']]
       # nodes_roms['lat'] = [nodes_roms['lat']]
    
    '''Calculate the distance seperation'''

    #dist_roms = distance((nodes_drifter['lat'][-1],nodes_drifter['lon'][-1]),(nodes_roms['lat'][-1],nodes_roms['lon'][-1]))
    dist_fvcom = distance((nodes_drifter['lat'][-1],nodes_drifter['lon'][-1]),(nodes_fvcom['lat'][-1],nodes_fvcom['lon'][-1]))
    #print 'The seperation of roms was %f and of fvcom was %f kilometers for drifter %s' % (dist_roms[0], dist_fvcom[0], ID )

    ''' set latitude and longitude arrays for basemap'''

    lonsize = [min_data(nodes_drifter['lon'],nodes_fvcom['lon']),
             max_data(nodes_drifter['lon'],nodes_fvcom['lon'])]
    latsize = [min_data(nodes_drifter['lat'],nodes_fvcom['lat']),
             max_data(nodes_drifter['lat'],nodes_fvcom['lat'])]
             
    diff_lon = (lonsize[0]-lonsize[1])*4
    diff_lat = (latsize[1]-latsize[0])*4
    
    lonsize = [lonsize[0]-diff_lon,lonsize[1]+diff_lon]
    latsize = [latsize[0]-diff_lat,latsize[1]+diff_lat]
           
    ''' Plot the drifter track, model outputs form fvcom and roms, and the basemap'''
      
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #draw_basemap(fig, ax, lonsize, latsize)
    ax.plot(nodes_drifter['lon'],nodes_drifter['lat'],'ro-',label='drifter')
    ax.plot(nodes_fvcom['lon'],nodes_fvcom['lat'],'yo-',label='fvcom')
    #ax.plot(nodes_roms['lon'],nodes_roms['lat'], 'go-', label='roms')
    ax.plot(nodes_drifter['lon'][0],nodes_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
    plt.title('ID: {0} {1} {2} days'.format(ID, starttime.strftime("%Y-%m-%d"), days))
    plt.legend(loc='lower right')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
    plt.savefig('plots/'+str(ID)+'.png')
    
