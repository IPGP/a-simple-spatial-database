#!/usr/bin/python3
# -*- coding:utf-8 -*-

import argparse
import os
import sys
import json

# createindex.py - Generate index.html for a-simple-spatial-database interface
# Copyright (C) 2020 Arthur Delorme
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

# (Contact: delorme@ipgp.fr)

print('''createindex.py Copyright (C) 2020 Arthur Delorme
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute
it under certain conditions.
See the GNU General Public License for more details.''')

parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=("Generate index.html for a-simple-spatial-database "
            "interface")
    )
parser.add_argument('--bing_maps_key', type=str,
    help="your Bing Maps API key (if not provided, OpenStreetMap will be used)")
parser.add_argument('--title', type=str,
    help="to customize the web page title")
args = parser.parse_args()

# Ask wether the script should delete itself or not
print(("\nFor safety reasons, this script ({}) "
        "should be deleted after the run.").format(
            os.path.basename(sys.argv[0])
        )
    )
while True:
    can_self_destructs = input(("Do you allow it to delete itself during the "
        "process? (y/n): "))
    if can_self_destructs not in ('y', 'n'):
        print("Please answer by yes or no (y/n).")
    else:
        self_destructs = True
        if can_self_destructs == 'n': 
            self_destructs = False
        break

# Scan the data directory
geojson_files = {}
for f in os.listdir('data'):
    if f.endswith('.geojson'):
        if ' ' in f:
            sys.exit(('Error with "{}": whitespaces not allowed in '
                'the GeoJSON file names'.format(f)))
        with open('data/'+f) as geojson_f:
            data = json.load(geojson_f)
            type = data['features'][0]['properties']['type']
            geometry_type = data['features'][0]['geometry']['type']
        if geometry_type not in ['Point', 'Polygon']:
            sys.exit(('Error with "{}": geometry type is not supported '
                '(only Point and Polygon are)'))
        geojson_files[f] = {
            'type': type,
            'geometry_type': geometry_type,
            'prefix': os.path.splitext(f)[0]
        }

# Load the color list
with open('colors.txt') as f:
    color_list = f.read().splitlines()

# Create file
with open('template_index.html') as f_in, open('index.html', 'w') as f_out:
    for l in f_in:
        if '<title>' in l and args.title:
            f_out.write('    <title>{}</title>\n'.format(args.title))
        elif '<h1>' in l and args.title:
            f_out.write('<h1>{}</h1>\n'.format(args.title))
        elif 'leaflet-bing-layer' in l and args.bing_maps_key:
            f_out.write('    {}\n'.format(l.split('--')[1].strip()))
        elif '//bing_maps' in l and args.bing_maps_key:
            if 'your_bing_maps_key' in l:
                f_out.write("    key = '{}';\n".format(args.bing_maps_key))
            else:
                f_out.write(l.replace('//bing_maps', ''))
        elif '//openstreetmap' in l and not args.bing_maps_key:
            f_out.write(l.replace('//openstreetmap', ''))
        elif '<!-- YOUR_DATA -->' in l: # HTML part
            for f in geojson_files:
                f_out.write(('    <link rel="{}" type="application/json" '
                        'href="data/{}">\n'.format(
                            geojson_files[f]['type'],
                            f
                        )
                    ))
        elif '// --> YOUR_DATA <--' in l: #JS part
            prefix_list = []
            for f in geojson_files:
                prefix = geojson_files[f]['prefix']
                prefix_list.append(prefix)
                f_out.write('    var {} = {{}};\n'.format(prefix))
            f_out.write('    var allLayers = [{}];\n'.format(
                    ', '.join(prefix_list)
                ))
            for i, f in enumerate(geojson_files):
                color = color_list[i]
                if geojson_files[f]['geometry_type'] == 'Point':
                    f_out.write("    addMarkerLayer('{}', {}, '{}');\n".format(
                            geojson_files[f]['type'],
                            geojson_files[f]['prefix'],
                            color
                        ))
                else:
                    f_out.write("    addPolygonLayer('{}', {}, '{}');\n".format(
                            geojson_files[f]['type'],
                            geojson_files[f]['prefix'],
                            color
                        ))
        else:
            f_out.write(l)

# Self-destruction of this initialization Python script, to avoid leaving a
# Python script on the web server
if not self_destructs:
    print(("\nYou have not allowed the script to delete itself.\nConsider "
        "deleting it manually or moving it to a safe location, outside the web "
        "server."))
else:
    print("\nThe script will now delete itself. Bye-bye!")
    os.remove(sys.argv[0])