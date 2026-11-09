# Project: DIRECTED
# Real World Lab: Danube Region
# Data:
# - Short description: pluvial flood simulations with SaferPlaces and related base data for Vienna
# - Original format: GeoTIFF and GeoPackage
# - Original crs: UTM zone 33N
#   → reprojecting all files to the crs the frontend is using (typically EPSG:3857) might lead to a performance boost
# The script prepares and uploads the data to GeoServer.
# Note on the GeoServer style: style sheets have to be uploaded separately to GeoServer, this script is not doing that.
# SLD files are available in the subfolder "geoserver_styles". They can simply be copy-pasted into the GeoServer UI
# mask, or this script could be extended.
import os

from utils import upload_coverage_to_geoserver, upload_geopackage_to_geoserver, update_style


if __name__ == "__main__":
    folder_original = ""
    geotiff_files = [
        "Vienna_lidar_2m_ViennaCenter_32633.tif",
        "Vienna_OpenLandMap_SOL_SOL_CLAY-WFRACTION_USDA-3A1A1A_M_v02_162021.tif",
        "Vienna_OpenLandMap_SOL_SOL_SAND-WFRACTION_USDA-3A1A1A_M_v02_162021.tif",
        "Vienna_WD_RAIN152452_Ref_RP25.tif",
        "Vienna_WD_RAIN164659_Ref_RP50.tif",
        "Vienna_WD_RAIN164612_Ref_RP100.tif",
        "Vienna_WD_RAIN164413_SSP245_RP25_2050.tif",
        "Vienna_WD_RAIN164745_SSP245_RP50_2050.tif",
        "Vienna_WD_RAIN164825_SSP245_RP100_2050.tif",
        "Vienna_WD_RAIN164413_SSP585_RP25_2050.tif",
        "Vienna_WD_RAIN164323_SSP585_RP50_2050.tif",
        "Vienna_WD_RAIN164223_SSP585_RP100_2050.tif",
        "Vienna_WD_RAIN164413_SSP245_RP25_2080.tif",
        "Vienna_WD_RAIN164323_SSP245_RP50_2080.tif",
        "Vienna_WD_RAIN164223_SSP245_RP100_2080.tif",
        "Vienna_WD_RAIN164323_SSP585_RP25_2080.tif",
        "Vienna_WD_RAIN164223_SSP585_RP50_2080.tif",
        "Vienna_WD_RAIN115927_SSP585_RP100_2080.tif"
    ]
    geopackage = "osm_buildings_162014.gpkg"
    # ------------------------------------------------------------- #
    geoserver_url = ""
    geoserver_user = ""
    geoserver_pw = ""
    for filename in geotiff_files:
        filename_absolute = os.path.join(folder_original, filename)
        layer_name = upload_coverage_to_geoserver(filename_absolute, geoserver_url, geoserver_user, geoserver_pw)
        if layer_name == "Vienna_lidar_2m_ViennaCenter_32633":
            geotiff_style = "lidar_elevation"
        elif layer_name.startswith("Vienna_WD_RAIN"):
            geotiff_style = "water_level_transparent"  # same style that Copenhagen flood layers use
        else:
            continue
        update_style(geotiff_style, layer_name, geoserver_url, geoserver_user, geoserver_pw)
    upload_geopackage_to_geoserver(os.path.join(folder_original, geopackage), geoserver_url, geoserver_user, geoserver_pw)
