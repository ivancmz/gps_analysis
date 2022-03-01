
import csv
import pandas
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import math
import numpy
import os
import struct
from matplotlib.patches import Circle
 



rEarth = 6371000 #radius of the earth in meters
# Input the file name.
# fname = raw_input("Enter file name WITHOUT extension: ")
# def latSign(value):
#     if value=='S':
#         return -1
#     else:
#         return 1

# def longSign(value):
#     if value=='W':
#         return -1
#     else:
#         return 1

# def cep_analysis(df_in, center_lat, center_lon, outfile):
#     df = df_in.copy()
    
#     plt.rc('xtick',labelsize=20)
#     plt.rc('ytick',labelsize=20)
#     #calcualte distance with law of Haversines
#     df['lat_rad'] = df['lat'].map(lambda x: math.radians(x))
#     df['lng_rad'] = df['lng'].map(lambda x: math.radians(x))

#     # print(df['lat_rad'])
#     # print(df['lng_rad'])

#     # df['phi_deg'] = df['lat_rad'].sub(math.radians(center_lat))
#     # df['lambda_deg'] = df['lng_rad'].sub(math.radians(center_lon))

#     # df['sin'] = numpy.sin(df['phi_deg']/2)
#     # df['cos'] = ((numpy.sin(df['phi_deg']/2)*(numpy.sin(df['phi_deg']/2)))) + ((numpy.cos(math.radians(center_lat)) * numpy.cos(df['lat_rad'])) * (numpy.sin(df['lambda_deg']/2) * numpy.sin(df['lambda_deg']/2)))

#     # df['a'] = ((numpy.sin(df['phi_deg']/2) * (numpy.sin(df['phi_deg']/2)))) + ((numpy.cos(center_lat) * numpy.cos(df['lat_rad'])) * (numpy.sin(df['lambda_deg']/2) * numpy.sin(df['lambda_deg']/2)))

#     # df['c'] = 2 * numpy.arctan2(numpy.sqrt(df['a']),numpy.sqrt(1-df['a']))

#     # df['d'] = rEarth * df['c']

#     #calculate delta lat/lng
#     df['deltalat'] = df['lat_rad'].sub(math.radians(center_lat))
#     df['deltalng'] = df['lng_rad'].sub(math.radians(center_lon))
#     #assume points are close together anc cald distances/angles
#     #df['dy'] = numpy.sin(df['deltalng'])
#     #df['dx'] = math.cos(math.radians(center_lat))*(df['lng']-center_lon)
#     #df['dx'] = numpy.cos(math.radians(center_lat)) * numpy.sin(df['lat_rad']) - numpy.sin(math.radians(center_lat)) * numpy.cos(df['lat_rad']) * numpy.cos(df['deltalng'])

#     df['dy'] = df['deltalat']
#     df['dx'] = numpy.cos(math.radians(center_lat))*(df['deltalng'])

#     df['r'] = numpy.sqrt(numpy.power(df['dy'],2) + numpy.power(df['dx'],2))
#     df['rd'] = df['r'] * rEarth
#     df['angle'] = numpy.arctan2(df['dy'],df['dx'])
#     df['angle'] = df['angle'] + math.pi
#     df['angle_deg'] = df['angle'].map(lambda x : math.degrees(x))
#     df = df.sort_values(by='angle')

#     df['dy_m'] = numpy.sin(df['angle']) * df['rd']
#     df['dx_m'] = numpy.cos(df['angle']) * df['rd']
#     #df.to_csv("test_out.csv")
#     #Calculate CEP Here
#     dx_extreme = df['dx_m'].abs().max()
#     dy_extreme = df['dy_m'].abs().max()
#     if dx_extreme > dy_extreme:
#         ax_extreme = dx_extreme
#     else:
#         ax_extreme = dy_extreme

#     sigma_dx = df['dx_m'].std()
#     sigma_dy = df['dy_m'].std()
#     radius_CEP = (0.56*sigma_dx) + (0.62*sigma_dy)
#     radius_2DRMS = 2*numpy.sqrt(sigma_dx**2 + sigma_dy**2)
#     print("CEP = " + str(radius_CEP))
#     print("2DRMS = " + str(radius_2DRMS))

#     #Draw Circles for Plotting
#     cir_CEP = plt.Circle((0,0),radius_CEP,color='forestgreen',alpha=0.2)
#     cir_2DRMS = plt.Circle((0,0),radius_2DRMS,color='tomato',alpha=0.2)
#     #patches.append(CEP_circle)
#     #patches.append(2DRMS_circle)

#     #custom legend definition
#     labels = [plt.Circle((0,0),0.005,color='forestgreen',alpha=0.2),plt.Circle((0,0),0.005,color='tomato',alpha=0.2),plt.Line2D((0,1),(0,0),color='dodgerblue',marker='o',linestyle='')]
#     descriptions = ['CEP = ' + str(radius_CEP),'2DRMS = ' + str(radius_2DRMS),'Fix Distance From True Position']
#     #p = PatchCollection(patches,alpha=0.4)

#     fig, ax1 = plt.subplots(figsize=(20,20))

#     sc=ax1.scatter(df['dx_m'],df['dy_m'],s=50,color='dodgerblue')

#     ax1.grid(True)
#     #ax1.legend(loc='upper left',prop={'size':'24'})
#     ax1.set_facecolor('whitesmoke')
#     ax1.add_artist(cir_2DRMS)
#     ax1.add_artist(cir_CEP)
#     ax1.legend(labels,descriptions,numpoints=1,markerscale=2,prop={'size': 24})
#     ax1.set_xlim([-ax_extreme,ax_extreme])
#     ax1.set_ylim([-ax_extreme,ax_extreme])
#     ax1.set_xlabel('Distance (m)')
#     ax1.set_ylabel('Distance (m)')
#     ax1.xaxis.label.set_size(24)
#     ax1.yaxis.label.set_size(24)
#     axes = plt.gca()
#     plt.title('CEP {0}'.format(outfile),fontsize=24,weight='bold')
#     plt.savefig(outfile+".png",dpi=300)

# # --------------------------------------------------------------------
# styles = """	
# 		<Style id="s_marca_{0}_hl">
# 		<IconStyle>
# 			<color>{2}</color>
# 			<scale>0.945455</scale>
# 			<Icon>
# 				<href>http://maps.google.com/mapfiles/kml/paddle/{1}.png</href>
# 			</Icon>
# 			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
# 		</IconStyle>
# 		<ListStyle>
# 			<ItemIcon>
# 				<href>http://maps.google.com/mapfiles/kml/paddle/{1}-lv.png</href>
# 			</ItemIcon>
# 		</ListStyle>
# 	</Style>
# 	<Style id="s_marca_{0}">
# 		<IconStyle>
# 			<color>{2}</color>
# 			<scale>0.8</scale>
# 			<Icon>
# 				<href>http://maps.google.com/mapfiles/kml/paddle/{1}.png</href>
# 			</Icon>
# 			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
# 		</IconStyle>
# 		<ListStyle>
# 			<ItemIcon>
# 				<href>http://maps.google.com/mapfiles/kml/paddle/{1}-lv.png</href>
# 			</ItemIcon>
# 		</ListStyle>
# 	</Style>
# 	<StyleMap id="m_marca_{0}">
# 		<Pair>
# 			<key>normal</key>
# 			<styleUrl>#s_marca_{0}</styleUrl>
# 		</Pair>
# 		<Pair>
# 			<key>highlight</key>
# 			<styleUrl>#s_marca_{0}_hl</styleUrl>
# 		</Pair>
# 	</StyleMap>
# """



centros_db = pandas.read_csv('centros.csv')
centros_db.set_index('grupo')

relaciones_db = pandas.read_csv('relacion.csv')

db = pandas.read_csv('tramas_export_1644927200787.csv')

db['lng'] = db['longitude'].where(db['ns'] == 'S', -1*db['longitude'])
db['lat'] = db['latitude'].where(db['ew'] == 'W', -1*db['latitude'])


# id;etiqueta;modulo;grupo;color

fulldb = db.set_index('deviceId').join(relaciones_db.set_index('id'))

has_location =  fulldb['eventLength']>77
loc_db = fulldb[has_location]

loc_db.to_csv('out.csv',index=False)

""" for grupo in range(1,4):
    for modulo in ['LC76F','L76LB']:
        has_grupo = loc_db['grupo']==grupo
        grupo_db = loc_db[has_grupo]
        has_modulo = grupo_db['modulo']==modulo
        grupo_modulo_db = grupo_db[has_modulo]
        outfile = 'Grupo{0}_{1}'.format(grupo,modulo)
        print(outfile)
        cep_analysis(grupo_modulo_db, centros_db.at[grupo-1,'center_lat'], centros_db.at[grupo-1,'center_lon'], outfile)
        outfile = 'Grupo{0}_{1}.kml'.format(grupo,modulo)
        with open(outfile, 'w') as f:
            #Writing the kml file.
            f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
            f.write("<Document>\n")
            f.write("   <name>"+outfile+"</name>\n")
            for index, row in relaciones_db.iterrows():
                f.write(styles.format(row['modulo']+row['etiqueta'],row['etiqueta'],row['color']))
            for index, row in grupo_modulo_db.iterrows():
                if int(row['eventLength'])>77 and (row['modulo']==modulo):
                    f.write("   <Placemark>\n")
                    # f.write("       <name>" + str(row['satellites']) + "</name>\n")
                    # f.write("       <description>" + str(row[0]) + "</description>\n")
                    f.write("       <Point>\n")
                    f.write("           <coordinates>" + str(row['lng']) + "," + str(row['lat']) + "," + str(row['altitude']) + "</coordinates>\n")
                    f.write("       </Point>\n")
                    f.write("       <styleUrl>#m_marca_{0}</styleUrl>\n".format(row['modulo']+row['etiqueta']))
                    f.write("   </Placemark>\n")
            f.write("</Document>\n")
            f.write("</kml>\n")
 """