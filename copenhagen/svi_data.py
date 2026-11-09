# Project: DIRECTED
# Real World Lab: The Capital Region of Denmark
# Data:
# - Short description: Social Vulnerability Index data for Roskilde Fjord
# - Original format: Shapefile
# - Original crs: EPSG:3044
# - New format: same as original
# - New crs: same as original
#   → reprojecting all files to the crs the frontend is using (typically EPSG:3857) might lead to a performance boost
# Note on the GeoServer style: style sheets have to be uploaded separately to GeoServer, this script is not doing that.
# SLD files are available in the subfolder "geoserver_styles". They can simply be copy-pasted into the GeoServer UI
# mask, or this script could be extended.
import os

from utils import upload_shapefile_to_geoserver, update_style


if __name__ == "__main__":
    geoserver_url = ""
    geoserver_user = ""
    geoserver_pw = ""
    shp_file = "roskildeSVI.zip"
    style = "svi_copenhagen"

    upload_shapefile_to_geoserver(shp_file, geoserver_url, geoserver_user, geoserver_pw)

    layer_name = os.path.splitext(os.path.basename(shp_file))[0]
    update_style(style, layer_name, geoserver_url, geoserver_user, geoserver_pw)
