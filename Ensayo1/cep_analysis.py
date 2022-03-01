import pandas as pd
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy
import os
import struct
from matplotlib.patches import Circle
#from geopy import distance

plt.rc('xtick',labelsize=20)
plt.rc('ytick',labelsize=20)

rEarth = 6371000 #radius of the earth in meters

# fpath = input("enter path where data is located: ")
# fpath = os.path.normpath(fpath)

#ifilein = input("enter name of gps log file: ")

outplot = "resultado_cep" # input("enter name for plot output: ")

# Parking Kepar
# center_lat = 41.643614 # float(input("Enter latitude of CEP Center: "))
# center_lon = -0.763253 # float(input("Enter longitude of CEP Center: "))

db = pd.read_csv('tramas_export_1644927200787.csv', delimiter=',')

db['lng'] = db['longitude'].where(db['ns'] == 'S', -1*db['longitude'])
db['lat'] = db['latitude'].where(db['ew'] == 'W', -1*db['latitude'])

has_location =  db['eventLength']>77
df = db[has_location]

# cols = ['datetime','lat','lng','alt','valid']

# df = pd.DataFrame()
# df_raw = pd.DataFrame()

# """
# for subdir,dirs,files in os.walk(fpath):
#     for name in files:
#         #print("merging files in dir " + os.path.join(fpath,name))
#         print(os.path.join(fpath,name))
#         try:
#             wifi_df = pd.read_csv(os.path.join(fpath,name),header=None,names=wifi_cols)
#             if df.empty:
#                 df = wifi_df
#             else:
#                 df = pd.concat([df,wifi_df])
#         except:
#             print("Unable to merge file " + str(name))
# """
# #uncomment below for windows
# #df_raw = pd.read_csv(fpath+"\\"+filein,header=None,names=cols)
# #uncomment below for linux
# df_raw = pd.read_csv(fpath+"/"+filein,header=None,names=cols)

# df_raw['datetime'] = pd.to_datetime(df_raw['datetime'],unit='s')

# df = df_raw[df_raw['lat'].astype(str) != 'NOFIX']
# df[['lat','lng','alt']] = df[['lat','lng','alt']].apply(pd.to_numeric, errors='coerce')


# #center_lat = df['lat'].mean()
# #center_lon = df['lng'].mean()


def describe_data(data):
    data = data[data != 0]
    data.dropna(inplace=True)
    print("count:   " + str(len(data)) )
    print("mean:    " + str(numpy.mean(data)) )
    print("std:     " + str(numpy.std(data)) )
    print("min:     " + str(numpy.min(data)) )
    print("max:     " + str(numpy.max(data)) )

def cep_analysis(df_in, center_lat, center_lon):
    df = df_in.copy()
    #calcualte distance with law of Haversines
    df['lat_rad'] = df['lat'].map(lambda x: math.radians(x))
    df['lng_rad'] = df['lng'].map(lambda x: math.radians(x))

    # df['phi_deg'] = df['lat_rad'].sub(math.radians(center_lat))
    # df['lambda_deg'] = df['lng_rad'].sub(math.radians(center_lon))

    # df['sin'] = numpy.sin(df['phi_deg']/2)
    # df['cos'] = ((numpy.sin(df['phi_deg']/2)*(numpy.sin(df['phi_deg']/2)))) + ((numpy.cos(math.radians(center_lat)) * numpy.cos(df['lat_rad'])) * (numpy.sin(df['lambda_deg']/2) * numpy.sin(df['lambda_deg']/2)))

    # df['a'] = ((numpy.sin(df['phi_deg']/2) * (numpy.sin(df['phi_deg']/2)))) + ((numpy.cos(center_lat) * numpy.cos(df['lat_rad'])) * (numpy.sin(df['lambda_deg']/2) * numpy.sin(df['lambda_deg']/2)))

    # df['c'] = 2 * numpy.arctan2(numpy.sqrt(df['a']),numpy.sqrt(1-df['a']))

    # df['d'] = rEarth * df['c']
    # df
    #calculate delta lat/lng
    df['deltalat'] = df['lat_rad'].sub(math.radians(center_lat))
    df['deltalng'] = df['lng_rad'].sub(math.radians(center_lon))
    #assume points are close together anc cald distances/angles
    #df['dy'] = numpy.sin(df['deltalng'])
    #df['dx'] = math.cos(math.radians(center_lat))*(df['lng']-center_lon)
    #df['dx'] = numpy.cos(math.radians(center_lat)) * numpy.sin(df['lat_rad']) - numpy.sin(math.radians(center_lat)) * numpy.cos(df['lat_rad']) * numpy.cos(df['deltalng'])

    df['dy'] = df['deltalat']
    df['dx'] = numpy.cos(math.radians(center_lat))*(df['deltalng'])

    df['r'] = numpy.sqrt(numpy.power(df['dy'],2) + numpy.power(df['dx'],2))
    df['rd'] = df['r'] * rEarth
    df['angle'] = numpy.arctan2(df['dy'],df['dx'])
    df['angle'] = df['angle'] + math.pi
    df['angle_deg'] = df['angle'].map(lambda x : math.degrees(x))
    df = df.sort_values(by='angle')

    df['dy_m'] = numpy.sin(df['angle']) * df['rd']
    df['dx_m'] = numpy.cos(df['angle']) * df['rd']
    df.to_csv("test_out.csv")
    #Calculate CEP Here
    dx_extreme = df['dx_m'].abs().max()
    dy_extreme = df['dy_m'].abs().max()
    if dx_extreme > dy_extreme:
        ax_extreme = dx_extreme
    else:
        ax_extreme = dy_extreme

    sigma_dx = df['dx_m'].std()
    sigma_dy = df['dy_m'].std()
    radius_CEP = (0.56*sigma_dx) + (0.62*sigma_dy)
    radius_2DRMS = 2*numpy.sqrt(sigma_dx**2 + sigma_dy**2)
    print("CEP = " + str(radius_CEP))
    print("2DRMS = " + str(radius_2DRMS))

    #Draw Circles for Plotting
    cir_CEP = plt.Circle((0,0),radius_CEP,color='forestgreen',alpha=0.2)
    cir_2DRMS = plt.Circle((0,0),radius_2DRMS,color='tomato',alpha=0.2)
    #patches.append(CEP_circle)
    #patches.append(2DRMS_circle)

    #custom legend definition
    labels = [plt.Circle((0,0),0.005,color='forestgreen',alpha=0.2),plt.Circle((0,0),0.005,color='tomato',alpha=0.2),plt.Line2D((0,1),(0,0),color='dodgerblue',marker='o',linestyle='')]
    descriptions = ['CEP = ' + str(radius_CEP),'2DRMS = ' + str(radius_2DRMS),'Fix Distance From True Position']
    #p = PatchCollection(patches,alpha=0.4)

    fig, ax1 = plt.subplots(figsize=(20,20))

    sc=ax1.scatter(df['dx_m'],df['dy_m'],s=50,color='dodgerblue')

    ax1.grid(True)
    #ax1.legend(loc='upper left',prop={'size':'24'})
    ax1.set_facecolor('whitesmoke')
    ax1.add_artist(cir_2DRMS)
    ax1.add_artist(cir_CEP)
    ax1.legend(labels,descriptions,numpoints=1,markerscale=2,prop={'size': 24})
    ax1.set_xlim([-ax_extreme,ax_extreme])
    ax1.set_ylim([-ax_extreme,ax_extreme])
    ax1.set_xlabel('Distance (m)')
    ax1.set_ylabel('Distance (m)')
    ax1.xaxis.label.set_size(24)
    ax1.yaxis.label.set_size(24)
    axes = plt.gca()
    plt.title('GPS CEP',fontsize=24,weight='bold')
    plt.savefig(outplot+".png",dpi=300)

#df.to_csv(fpath+"\\"+outplot+"_wifi_df.csv")

cep_analysis(df, 41.643614, -0.763253)
