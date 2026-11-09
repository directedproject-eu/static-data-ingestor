# Project: DIRECTED
# Real World Lab: The Capital Region of Denmark
# Data:
# - Short description: coastal flood damage and associated uncertainty data
# - Original format: GeoTIFF (damage data), GPKG (uncertainty data)
# - Original crs: ETRS89 / UTM zone 32N
# - New format: same as original
# - New crs: same as original
#   → reprojecting all files to the crs the frontend is using (typically EPSG:3857) might lead to a performance boost
# Note on the GeoServer style: style sheets have to be uploaded separately to GeoServer, this script is not doing that.
# SLD files are available in the subfolder "geoserver_styles". They can simply be copy-pasted into the GeoServer UI
# mask, or this script could be extended.
import os

from utils import upload_coverage_to_geoserver, upload_geopackage_to_geoserver, update_style


if __name__ == "__main__":
    geoserver_url = ""
    geoserver_user = ""
    geoserver_pw = ""
    folder_damage = "mean_damage"
    style_damage = "mean_flood_damage"
    folder_uncertainty= "mean_uncertainty"
    style_uncertainty = "mean_uncertainty"

    # Damage data
    for filename in os.listdir(folder_damage):
        split = os.path.splitext(os.path.basename(filename))
        root = split[0]
        ext = split[-1]

        if  ext == ".geotiff":
            filename_absolute = os.path.join(folder_damage, filename)
            print(f"Upload file {filename_absolute} to GeoServer")
            upload_coverage_to_geoserver(filename_absolute, geoserver_url, geoserver_user, geoserver_pw)
            print(f"Update style")
            update_style(style_damage, root, geoserver_url, geoserver_user, geoserver_pw)

    # Uncertainty data
    for filename in os.listdir(folder_uncertainty):
        split = os.path.splitext(os.path.basename(filename))
        root = split[0]
        ext = split[-1]
        if ext == ".gpkg":
            filename_absolute = os.path.join(folder_damage, filename)
            print(f"Upload file {filename_absolute} to GeoServer")
            upload_geopackage_to_geoserver(filename_absolute, geoserver_url, geoserver_user, geoserver_pw)
            print(f"Update style")
            update_style(style_uncertainty, root, geoserver_url, geoserver_user, geoserver_pw)
