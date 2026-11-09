# Project: DIRECTED
# Real World Lab: Danube Region
# Data:
# - Short description: future fluvial flood return period shifts due to climate change simulated with the Danube Model
# - Original format: GeoPackage
# - Original crs: EPSG:4258
#   → reprojecting all files to the crs the frontend is using (typically EPSG:3857) might lead to a performance boost
# Detailed description:
# Originally, the data is stored in a single file. Each feature in the file has several attributes corresponding
# to different SSP scenarios and return periods. For the GeoServer upload, these are separated into individual files.
# This is done with the shell script "danube_model_flood_return_period_shift_split_files.sh".
# Note on the GeoServer style: style sheets have to be uploaded separately to GeoServer, this script is not doing that.
# SLD files are available in the subfolder "geoserver_styles". They can simply be copy-pasted into the GeoServer UI
# mask, or this script could be extended.

import os

from utils import upload_geopackage_to_geoserver, update_style


if __name__ == "__main__":
    url = "" # GeoServer url
    user = ""
    pw = ""

    names = [
        "r010s_370",
        "r025s_370",
        "r050s_370",
        "r100s_370",
        "r250s_370",
        "r010s_585",
        "r025s_585",
        "r050s_585",
        "r100s_585",
        "r250s_585"
    ]

    base_path = "<my-base-path>"  # path where the gpkg files are stored
    prefix = "danube_flood_return_period_shifts"
    ext = "gpkg"
    style = "fluvial_flood_return_period_shifts"  # name of the GeoServer style; has to be created separately
    gpkg_files = [os.path.join(base_path, f"{prefix}_{n}.{ext}") for n in names]
    for file in gpkg_files:
        layer = os.path.basename(file).strip(".gpkg")
        print(layer)
        upload_geopackage_to_geoserver(file, url, user, pw)
        update_style(style, layer, url, user, pw)
