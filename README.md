# a-simple-spatial-database

This is an attempt to share the work that I have done, by developing an interface to share spatial data in our team.

It is largely based on [Leaflet](https://leafletjs.com), a great open source JavaScript library! But not only.

The web interface shows a map, on which you can display each dataset as a layer. When you select data from the map, the results are listed below the map, dynamically.

The idea is to keep it simple: only a basic Linux web server is needed. The interface consists in HTML and JavaScript, and GeoJSON files as a database. So no PHP, no SQL, etc. Also, to facilitate installation and avoid compatibility issues, the external libraries used in the code are also provided in this repository (in the `external` directory).

## External libraries (provided in this repository)

- [Leaflet](https://leafletjs.com)
- [Turf.js](http://turfjs.org)
- [jQuery](https://jquery.com)
- [jQuery UI](https://jqueryui.com)

Leaflet plugins:
- [Leaflet.draw](http://leaflet.github.io/Leaflet.draw/docs/leaflet-draw-latest.html)
- [leaflet-bing-layer](https://github.com/digidem/leaflet-bing-layer)
- [Leaflet.Grid](https://github.com/jieter/Leaflet.Grid)
- [Leaflet.GestureHandling](https://github.com/elmarquis/Leaflet.GestureHandling)

## Database

You need to provide one [GeoJSON](https://geojson.org) file per dataset. By dataset is meant a set of homogeneous data. For example, one file listing images of one satellite (or multiple satellites, as long as they share the same family of parameters), one file listing GPS stations, etc.

A very handy tool, `ogr2ogr`, is available in GDAL for converting between formats (including GeoJSON).

#### About the GeoJSON files
- Additional requirements:
  - For the moment, among the types of geometry proposed in GeoJSON, only two are available: `Polygon` and `Point`.
  - The `properties` member of each Feature object **must** contain a `type` property. Its value **must** be the same for each object. For example, it could be the name of the satellite or "GPS station".

- "Special" `properties` (optional):
  - `date` : if the data have a date information, using `date` as the property name will allow to filter the results by date.
  - `url` : if you provide a link to download the data, using `url` as the property name will make the URL prettier.
  - `kmz` : if you offer KMZ files for download, using `kmz` as the property name will make the URL prettier too.
  - `preview` : if you want to display a preview image, using `preview` as the property name will make the preview prettier.
  - If you want to display the coordinates of the four corners of an image, use the following property names: `lon_tl` (for top left), `lat_tl`, `lon_tr`, `lat_tr`, `lon_br`, `lat_br`, `lon_bl`, `lat_bl`.
  - When you click on an object on the map, a popup displays the `type` property, and also the `date` and/or `name` properties, if they exist in the GeoJSON file.

(Two files are provided in the `data` directory, as examples.)

## Installation

1) Download the files and move them to a dedicated directory, in the `DocumentRoot` of your web server (typically, you will create this directory in `/var/www/html/`).

2) Place the GeoJSON files in the **`data`** directory (two files are provided as examples).

3) Run the **`createindex.py`** initialization script. This will generate `index.html`, which is the core part of the interface.

```
createindex.py [-h] [--true_run] [--bing_maps_key BING_MAPS_KEY] [--title TITLE]
```
Optional arguments:
```
-h, --help                          show this help message and exit
--true_run                          add this to really run the script (the script will purposely delete
                                        itself during the process)
--bing_maps_key BING_MAPS_KEY       your Bing Maps API key (if not provided, OpenStreetMap will be used)
--title TITLE                       to customize the web page title
```

And this is it!

For security reasons, the `createindex.py` script self-destructs at the end of its execution. This is to avoid potential security breaches on the web server. In the future, if you need to update the interface, to add a new dataset for example, just keep a copy in a safe directory (i.e. not accessible to the client) or download it again from here.
