import csv
# Input the file name.
# fname = raw_input("Enter file name WITHOUT extension: ")
def latSign(value):
    if value=='S':
        return -1
    else:
        return 1

def longSign(value):
    if value=='W':
        return -1
    else:
        return 1


styles = """	<Style id="s_marca_a_hl">
		<IconStyle>
			<scale>0.945455</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/paddle/A.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<ListStyle>
			<ItemIcon>
				<href>http://maps.google.com/mapfiles/kml/paddle/A-lv.png</href>
			</ItemIcon>
		</ListStyle>
	</Style>
	<Style id="s_marca_a">
		<IconStyle>
			<scale>0.8</scale>
			<Icon>
				<href>http://maps.google.com/mapfiles/kml/paddle/A.png</href>
			</Icon>
			<hotSpot x="32" y="1" xunits="pixels" yunits="pixels"/>
		</IconStyle>
		<ListStyle>
			<ItemIcon>
				<href>http://maps.google.com/mapfiles/kml/paddle/A-lv.png</href>
			</ItemIcon>
		</ListStyle>
	</Style>
	<StyleMap id="m_marca_a">
		<Pair>
			<key>normal</key>
			<styleUrl>#s_marca_a</styleUrl>
		</Pair>
		<Pair>
			<key>highlight</key>
			<styleUrl>#s_marca_a_hl</styleUrl>
		</Pair>
	</StyleMap>
"""

with open("tramas_export_1644257289215.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    with open('csv2kml.kml', 'w') as f:
        #Writing the kml file.
        f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
        f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
        f.write("<Document>\n")
        f.write("   <name> tramas_export_1644257289215.kml</name>\n")
        f.write(styles)
        for row in reader:
            if int(row['eventLength'])>77:
                f.write("   <Placemark>\n")
                #f.write("       <name>" + str(row[1]) + "</name>\n")
                #f.write("       <description>" + str(row[0]) + "</description>\n")
                f.write("       <Point>\n")
                f.write("           <coordinates>" + str(longSign(row['ew'])*float(row['longitude'])) + "," + str(latSign(row['ns'])*float(row['latitude'])) + "," + str(row['altitude']) + "</coordinates>\n")
                f.write("       </Point>\n")
                f.write("       <styleUrl>#m_marca_a</styleUrl>\n")
                f.write("   </Placemark>\n")
        f.write("</Document>\n")
        f.write("</kml>\n")
