''' 
This routine compares MULTIPLE drifter tracks to MULTIPLE model-derived tracks
It is a enhanced version of Jian's track_cmp.py routine as modified by Conner Warren in summer 2014.
Many of the functions and variables were renamed to better reflect their tasks and identity. 
Some comments and adjustments by JiM and Bingwei.
In November 2014, we added the option to run the code backwards

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
from track_functions import get_drifter,get_fvcom,get_roms,draw_basemap,distance,uniquecolors
from makegrid import clickmap, points_between
st_run_time = datetime.now()

########## Step 1: Options ###########################
'''Three options to define track start 1) by drifters;
   2) user defined along a straight line(s); 3) clicking map'''
option=1
DAYS = 2                     # Length of time wanted in track
run_time = datetime(2013,6,20,12,0,0,0,pytz.UTC) 
MODEL = 'FVCOM'              # 'FVCOM', 'ROMS' or 'BOTH'
DEPTH = -1.                  # depth of drogue in meters
#OUTPUTDIR='/net/nwebserver/epd/ocean/MainPage/track/ccbay/'
png_dir = '/home/bling/Documents/track-figures/'
points = {'lats':[],'lons':[]}
###########  Step 2:Check more detail#########################
if option==1: # specified drifters
    # Default driftecr ID
    MODE = 'FORCAST'           # 'FORECAST' or 'HINDCAST'
    GRID = 'massbay'            # '30yr', 'massbaya', 'GOM3a', 'GOM3' or 'massbay'
    drifter_ids = ['115410701','118410701','108410712','108420701','110410711','110410712',
                   '110410713','110410714','110410715','110410716','114410701','115410701',
                   '115410702','119410714','135410701','110410713','119410716']  
elif option==2: # user specified pts
    track_way = 'forwards' # two options: forwards,backwards
    GRID = 'massbaya'     # '30yr', 'massbaya', 'GOM3a', 'GOM3' or 'massbay'
    (lat,lon)=points_between((41.729686, -70.636645), (41.686903, -70.665452),1)
    (lat2,lon2)=points_between((41.654465, -70.657109), (41.661779, -70.736143),1)
    #(lat3,lon3)=points_between((41.687952, -70.695588), (41.665847, -70.677392),0)   
    lat=lat+lat2#+lat3
    lon=lon+lon2#+lon3
    print 'You added %d points.' % len(lat)
elif option==3: # click on a map
    track_way = 'forwards' # two options: forwards,backwards
    GRID = 'massbaya'     # '30yr', 'massbaya', 'GOM3a', 'GOM3' or 'massbay'
    numpts=9 # at most added on the map
    [lon,lat]=clickmap(numpts) # gets lat/lon by clicking map
    print 'You added %d points.' % len(lat)
##################Step 3: executing ##################   
if option==1:
    drifter_ID = '140410701'
    # if raw data, use "drift_X.dat";if want to get drifter data in database, use "None"
    INPUT_DATA = 'drift_X.dat'   
    start_time = datetime(2014,11,26,11,50,0,0,pytz.UTC)
    end_time = start_time + timedelta(DAYS)
    drifter = get_drifter(drifter_ID, INPUT_DATA)# New drifter data or old drifter data
    dr_points = drifter.get_track(start_time,DAYS)
    st_point = (dr_points['lon'][-1],dr_points['lat'][-1])
    if MODEL in ('FVCOM','BOTH'):
        get_obj = get_fvcom(GRID)
        url_fvcom = get_obj.get_url(start_time,end_time)
        point = get_obj.get_track(st_point[0],st_point[1],DEPTH,url_fvcom)
    if MODEL in ('ROMS', 'BOTH'):
        get_obj = get_roms()
        url_roms = get_obj.get_url(start_time, end_time)
        point = get_obj.get_track(st_point[0],st_point[1],DEPTH,url_roms)
    points['lats'].extend(point['lat'])
    points['lons'].extend(point['lon'])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(point['lon'],point['lat'],'ro-',label='drifter')
    ax.plot(dr_points['lon'][-1],dr_points['lat'][-1],'c.',label='Startpoint',markersize=20)
    ax.annotate(drifter_ID, xy=(st_point),fontsize=6,xytext=(st_point[0]+0.03,st_point[1]+0.01),
                arrowprops=dict(arrowstyle="wedge")) #facecolor=colors[i]
    draw_basemap(fig, ax, points)
    plt.title('{0} {1}-days from {2} '.format(MODE,DAYS,start_time.strftime("%F %H:%M")))
    plt.legend(loc='lower right')
    plt.savefig(png_dir+"Drifter_track: %s"%(drifter_ID),dpi=200) #bbox_inches='tight'   
############################
if (option==2) | (option==3):
    obj_points = {'lat':[41.801167,41.807005],'lon':[-70.529587,-70.534930]}
    points['lats'].extend(obj_points['lat']); points['lons'].extend(obj_points['lon'])
    colors=uniquecolors(len(lat)) #config colors
    fig = plt.figure(figsize=(16,9))
    ax1 = fig.add_subplot(231); ax2 = fig.add_subplot(232); ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234); ax5 = fig.add_subplot(235); ax6 = fig.add_subplot(236)
    loax = [ax1,ax2,ax3,ax4,ax5,ax6]
    for j in range(6):   
        ax = loax[j]
        start_time = run_time + timedelta(j) 
        end_time = start_time + timedelta(DAYS)
        if track_way == 'backwards':
            end_time = run_time + timedelta(j) 
            start_time = end_time + timedelta(DAYS)
        p_file = open('ax%d_points.txt'%(j+1),'w')
        for i in range(len(lat)):
            print "ax{0}: {1}th point starting at {3} {2} for {4}days".format((j+1),(i+1),track_way,start_time.strftime("%D"),DAYS)
            stp_ID = 'Start%d' % (i+1)
            if MODEL in ('FVCOM','BOTH'):
                get_obj = get_fvcom(GRID)
                url_fvcom = get_obj.get_url(start_time,end_time)
                point = get_obj.get_track(lon[i],lat[i],DEPTH,url_fvcom)
            if MODEL in ('ROMS', 'BOTH'):
                get_obj = get_roms()
                url_roms = get_obj.get_url(start_time, end_time)
                point = get_obj.get_track(lon[i],lat[i],DEPTH,url_roms)
            
            points['lats'].extend(point['lat'])
            points['lons'].extend(point['lon'])
            #for p in point['lon']: points['lons'].append(p)
            for h in zip(point['lat'],point['lon']): p_file.write('%f,%f\n'%h)
            #Calculate the distance separation
            dist = distance((lat[i],lon[i]),(point['lat'][-1],point['lon'][-1]))    
            print 'The separation of %s is %f kilometers to %s'%(track_way,dist[0],stp_ID)
            ax.plot(point['lon'],point['lat'], '-',color=colors[i], linewidth=2)
            ax.annotate(stp_ID, xy=(lon[i],lat[i]),fontsize=6,xytext=(lon[i]+0.03,
                        lat[i]+0.01),arrowprops=dict(arrowstyle="wedge",facecolor=colors[i])) 
                        # connectionstyle="angle3,angleA=0,angleB=-90"        
        ax.plot(obj_points['lon'],obj_points['lat'],'c.',markersize=8)
        ax.text(obj_points['lon'][0],obj_points['lat'][0],'Trash',fontsize=8,rotation=0)
        #plt.legend(loc='lower right')
        '''if i==3 or i==4 or i==5:
            ax.set_xlabel('longitude')
        if i==0 or i==3:
            ax.set_ylabel('latitude')'''
        ax.set_title("%s: %s - %s"%(track_way,start_time.strftime("%m/%d/%Y"),end_time.strftime("%m/%d/%Y")))
        p_file.close()                            
    for ax in loax:
        draw_basemap(fig, ax, points)
    plt.savefig(png_dir+"%s_%s-days_from_Buzzards_Bay"%(track_way,DAYS),dpi=400) #,bbox_inches='tight'
##################################################################
en_run_time = datetime.now()
print 'Take '+str(en_run_time-st_run_time)+' running the code. End at '+str(en_run_time)
plt.show()
