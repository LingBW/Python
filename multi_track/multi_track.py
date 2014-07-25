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
    
