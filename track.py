''' 
This routine compares MULTIPLE drifter tracks to MULTIPLE model-derived tracks
It is a enhanced version of Jian's track_cmp.py routine as modified by Conner Warren in summer 2014.
Many of the functions and variables were renamed to better reflect their tasks and identity. 
Some comments and adjustments by JiM.

GENERAL NOTES:
    1. Hardcodes are at the beginning of the program or function
    2. If any major changes are made, the flowcharts MUST be updated
'''

#Step 1: Import modules
import sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta
from matplotlib import path
import calendar
import pytz
import pandas as pd
sys.path.append('../bin')
import netCDF4 
from track_functions import * # all homegrown functions needed for this routine

# Step 2: Hardcode constants
# some of the drifters apparently test by Conner
#drifter_ids = ['115410701','118410701','108410712','108420701','110410711','110410712','110410713','110410714',
#               '110410715','110410716','114410701','115410701','115410702','119410714','135410701','110410713','119410716']                                                  # Default drifter ID
drifter_ids = ['147420706']  # ['147420706', '146410702','148410723', '148410701','148410727', '148410729'] ['138410721']
USE = 'HINDCAST'             # 'FORECAST' or 'HIHDCAST'
FILENAME = 'drift_X.dat'              # if new data, use "drift_X.dat".
DEPTH = -1.                  # depth of drogue in meters
# starttime = datetime(2011,5,12,13,0,0,0,pytz.UTC)
starttime = None             # If it's None, use the current time.
DAYS = 1                     # Number or None. Length of time wanted in track, if not given, track to the last poistion of drifter.
MODEL = 'ROMS'               # 'FVCOM', 'ROMS' or 'BOTH'
GRID = 'GOM3'                # '30yr', 'GOM3' or 'massbay'(both 'GOM3' and 'massbay' are forecast), only used in fvcom.

for ID in drifter_ids:
    print "ID: ", ID
    drifter = get_drifter(ID, FILENAME)# New drifter data or old drifter data
    points_drifter = drifter.get_track(starttime,DAYS)
    if USE == 'HINDCAST':
        # adjust for the added 5 hours in the models
        if GRID == 'massbay':
           time1 = pytz.utc.localize(datetime.now().replace(hour=0,minute=0))-timedelta(days=3)
           # get starttime, and lon, lat
           if starttime:
               if starttime < time1:
                   raise Exception('start time should be later than time that 3days before today.')
               l1 = points_drifter['time']-points_drifter['time'][0]
               l2 = starttime - points_drifter['time'][0]
               index = np.where(abs(l1-l2)==min(abs(l1-l2)))[0][0]
               lon, lat = points_drifter['lon'][index], points_drifter['lat'][index]
           else:
               starttime = time1
               lon, lat = points_drifter['lon'][0], points_drifter['lat'][0]
           # get endtime
           if DAYS:
               endtime = starttime + timedelta(days=DAYS)
           else:
               endtime = points_drifter['time'][-1]
        else:                  # if '30yr' or 'GOM3'
            starttime = points_drifter['time'][0]
            endtime = points_drifter['time'][-1]
            lon, lat = points_drifter['lon'][0], points_drifter['lat'][0]
    elif USE == 'FORECAST':
        starttime = points_drifter['time'][-1]
        endtime = starttime + timedelta(days=DAYS) 
        lon, lat = points_drifter['lon'][-1], points_drifter['lat'][-1]

    # read data points from fvcom and roms websites and store them

    #set latitude and longitude arrays for basemap
    lonsize = [min(points_drifter['lon']), max(points_drifter['lon'])]
    latsize = [min(points_drifter['lat']), max(points_drifter['lat'])]
    diff_lon = (lonsize[0]-lonsize[1])*4
    diff_lat = (latsize[1]-latsize[0])*4
    lonsize = [lonsize[0]-diff_lon,lonsize[1]+diff_lon]
    latsize = [latsize[0]-diff_lat,latsize[1]+diff_lat]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    draw_basemap(fig, ax, lonsize, latsize)
    ax.plot(points_drifter['lon'],points_drifter['lat'],'ro-',label='drifter')
    ax.plot(points_drifter['lon'][0],points_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
    if MODEL in ('FVCOM', 'BOTH'):
        get_fvcom_obj = get_fvcom(GRID)
        url_fvcom = get_fvcom_obj.get_url(starttime, endtime)
        points_fvcom = get_fvcom_obj.get_track(lon,lat,DEPTH,url_fvcom)           # iterates fvcom's data
        dist_fvcom = distance((points_drifter['lat'][-1],points_drifter['lon'][-1]),(points_fvcom['lat'][-1],points_fvcom['lon'][-1]))
        print 'The separation of fvcom was %f kilometers for drifter %s' % (dist_fvcom[0], ID )
        ax.plot(points_fvcom['lon'],points_fvcom['lat'],'yo-',label='fvcom')
    if MODEL in ('ROMS', 'BOTH'):
        get_roms_obj = get_roms()
        url_roms = get_roms_obj.get_url(starttime, endtime)
        points_roms = get_roms_obj.get_track(lon, lat, DEPTH, url_roms)
        if type(points_roms['lat']) == np.float64:                             # ensures that the single point case still functions properly   
            points_roms['lon'] = [points_roms['lon']] 
            points_roms['lat'] = [points_roms['lat']]
        #Calculate the distance separation
        dist_roms = distance((points_drifter['lat'][-1],points_drifter['lon'][-1]),(points_roms['lat'][-1],points_roms['lon'][-1]))
        print 'The separation of roms was %f kilometers for drifter %s' % (dist_roms[0], ID)
        ax.plot(points_roms['lon'],points_roms['lat'], 'go-', label='roms')

    '''
    #Plot the drifter track, model outputs form fvcom and roms, and the basemap          
    fig = plt.figure()
    ax = fig.add_subplot(111)
    draw_basemap(fig, ax, lonsize, latsize)
    ax.plot(points_drifter['lon'],points_drifter['lat'],'ro-',label='drifter')
    ax.plot(points_fvcom['lon'],points_fvcom['lat'],'yo-',label='fvcom')
    ax.plot(points_roms['lon'],points_roms['lat'], 'go-', label='roms')
    '''
    # ax.plot(points_drifter['lon'][0],points_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
    plt.title('ID: {0}   {1}   {2} days'.format(ID, starttime.strftime("%Y-%m-%d"), DAYS))
    plt.legend(loc='lower right')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
    # plt.savefig('plots/'+MODEL+str(ID)+'.png')
    plt.savefig('ID-' + str(ID) +'-%s.png' % USE, dpi=200)
