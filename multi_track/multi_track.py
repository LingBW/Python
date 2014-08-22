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
from matplotlib import path
import pandas as pd
sys.path.append('../bin')
import netCDF4 
import track_functions  # all homegrown functions needed for this routine
from track_functions import *

# Step 2: Hardcode constants'''
# some of the drifters apparently test by Conner
#drifter_ids = ['115410701','118410701','108410712','108420701','110410711','110410712','110410713','110410714',
#               '110410715','110410716','114410701','115410701','115410702','119410714','135410701','110410713','119410716']                                                  # Default drifter ID
<<<<<<< HEAD
drifter_ids = ['146410702']  # ['147420706']
FILENAME = 'drift_X.dat'            # if new data, use this.
DEPTH = -1.                         # depth of drogue in meters
# starttime = datetime(2011,5,12,13,0,0,0,pytz.UTC)
starttime = None
DAYS = .5                           # length of time wanted in track
MODEL = 'ROMS'                     # model has to to 'FVCOM' or 'ROMS' or 'BOTH'
# If MODEL is 'FVCOM' or 'BOTH', you need to specify the grid used in fvcom.
GRID = '30yr'                       # gird has to be '30yr' or 'GOM3', or ''massbay

for ID in drifter_ids:
    print ID
    if FILENAME:
        drifter = get_drifter(ID, FILENAME)
    else:
        drifter = get_drifter(ID)
    if starttime:
        if DAYS:
            points_drifter = drifter.get_track(starttime,DAYS)
        else:
            points_drifter = drifter.get_track(starttime)
    else:
        points_drifter = drifter.get_track()
    # determine latitude, longitude, start, and end times of the drifter?    
    lon, lat = points_drifter['lon'][-1], points_drifter['lat'][-1]
    # adjust for the added 5 hours in the models
    starttime = points_drifter['time'][0]-timedelta(hours=5)
    endtime = points_drifter['time'][-1]-timedelta(hours=5)
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
        if GRID == 'GOM3':
            starttime = endtime
            endtime = starttime + timedelta(days = DAYS)
            lon, lat = points_drifter['lon'][-1], points_drifter['lat'][-1]
        get_fvcom_obj = get_fvcom(GRID)
        url_fvcom = get_fvcom_obj.get_url(starttime, endtime)
        print url_fvcom
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
    ax.plot(points_drifter['lon'][0],points_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
    plt.title('ID: {0}   {1}   {2} days'.format(ID, starttime.strftime("%Y-%m-%d"), DAYS))
    plt.legend(loc='lower right')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
    plt.savefig('plots/'+str(ID)+'.png')
=======
drifter_ids = ['110410711','139410701','138410701','135410701','110410713','118410701']

depth = -1. # depth of drogue in meters
days = .25 # length of time wanted in track
lat_incr = .1                                                                # Longitude increments displayed on the plot
lon_incr = .1                                                                # Longitude increments displayed on the plot
six_track = 0                                                                # Allows for use of the 6_tracks program
starttime = datetime(2011,5,12,13,0,0,0,pytz.UTC)

''' Setup plot '''
if six_track == 1:
    fig = plt.figure(figsize=(20,20))
    counter = 0

''' Retrieve the data'''
for ID in drifter_ids:
    
    nodes_drifter, nodes_roms, nodes_fvcom, lonsize, latsize, starttime = multi_track(ID, depth, days, lat_incr, lon_incr, starttime)

    if six_track == 0:

        ''' Plot the drifter track, model outputs form fvcom and roms, and the basemap'''           
      
        fig = plt.figure()
        ax = fig.add_subplot(111)
        draw_basemap(fig, ax, lonsize, latsize, lon_incr, lat_incr)
        ax.plot(nodes_drifter['lon'],nodes_drifter['lat'],'ro-',label='drifter')
        ax.plot(nodes_fvcom['lon'],nodes_fvcom['lat'],'yo-',label='fvcom')
        ax.plot(nodes_roms['lon'],nodes_roms['lat'], 'go-', label='roms')
        ax.plot(nodes_drifter['lon'][0],nodes_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
        plt.title('ID: {0}   {1}   {2} days'.format(ID, starttime.strftime("%Y-%m-%d"), days))
        plt.legend(loc='lower right')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.show()
        plt.savefig('plots/'+str(ID)+'_'+str(days)+'_days.png')
        
    else: 
        
        counter = counter + 1        
        
        ''' Plot the drifter track, model outputs from fvcom and roms, and the basemap'''           
      
        ax = fig.add_subplot(2,3,counter) 
        draw_basemap(fig, ax, lonsize, latsize,.1,.1)
        ax.plot(nodes_drifter['lon'],nodes_drifter['lat'],'ro-',label='drifter')
        ax.plot(nodes_fvcom['lon'],nodes_fvcom['lat'],'yo-',label='fvcom')
        ax.plot(nodes_roms['lon'],nodes_roms['lat'], 'go-', label='roms')
        ax.plot(nodes_drifter['lon'][0],nodes_drifter['lat'][0],'c.',label='Startpoint',markersize=20)
        plt.title('ID: {0}   {1}   {2} days'.format(ID, starttime.strftime("%Y-%m-%d"), days))

''' Plot the global figure elements'''
if six_track == 1:
    plt.legend(loc=(.9,.1))
    fig.text(.5, .05, 'Longitude', ha='center',size=16)
    fig.text(.05, .5, 'Latitude', ha='center', rotation='vertical',size=16)
    plt.show()
    plt.savefig('plots/6_tracks.png')
    
>>>>>>> upstream/master
