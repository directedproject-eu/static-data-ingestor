# Project: DIRECTED
# Real World Lab: Rhine-Erft Region
# Data:
# - Short description: dam break scenarios
# - Original format: NetCDF
# - Original crs: EPSG:25832
# - New format: GeoTIFF
# - New crs: EPSG:3857
# Detailed description:
# Dam break scenarios simulated with RIM2D. A docx report about the simulations is available next to the data.
# In total, six different scenarios have been simulated. This script is only configured for one of the scenarios, i.e.
# the HRB Eicherscheid base breach scenario.
# Note on the GeoServer styles: style sheets have to be uploaded manually to GeoServer, this script is not doing that.
# SLD files are available in the subfolder "geoserver_styles". They can simply be copy-pasted into the GeoServer UI
# mask, or this script could be extended.

import logging
import os
import re
import requests
from requests.auth import HTTPBasicAuth

from geo.Geoserver import Geoserver

from utils import upload_coverage_to_geoserver, netcdf_to_geotiff, get_gs_coverage_body

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def rename_file(file, new_base):
    pattern = r"(?:vel|wd)_(?:\d+|max|max_t)"
    match = re.search(pattern, file)
    if match:
        result = match.group(0)
        return new_base + result + ".tif"
    else:
        # initial water condition
        pattern = r"_IWD.nc"
        match = re.search(pattern, file)
        if match:
            return new_base + "wd_0.tif"
        else:
            logger.warning(f"Could not rename {file}")
            return None

def update_gs_styles(url, username, password, workspace = 'directed'):
    client = Geoserver(url, username=username, password=password)
    layers = client.get_layers(workspace=workspace)
    layer_names = [layer['name'] for layer in layers['layers']['layer']]
    for layer_name in layer_names:
        if "wd" in layer_name:
            style_name = "dam_break_wd"
        elif "vel" in layer_name:
            style_name = "dam_break_vel"
        else:
            continue
        try:
            layer = client.get_layer(layer_name)
            if layer['layer']['type'] == 'RASTER':
                client.publish_style(layer_name, style_name, workspace=workspace)
        except Exception as err:
            print(err)


def update_gs_band_names(base_url, username, password, workspace = 'directed'):
    headers = {
        "Content-Type": "application/json"
    }
    client = Geoserver(base_url, username=username, password=password)
    layers = client.get_layers(workspace=workspace)
    layer_names = [layer['name'] for layer in layers['layers']['layer']]
    for layer_name in layer_names:
        if "wd" in layer_name:
            band_name = "water_depth"
        elif "vel" in layer_name:
            band_name = "flow_velocity"
        else:
            continue
        try:
            layer = client.get_layer(layer_name)
            if layer['layer']['type'] == 'RASTER':
                url = f"{base_url}/rest/workspaces/{workspace}/coveragestores/{layer['layer']['name']}/coverages/{layer['layer']['name']}"
                requests.put(
                    url=url,
                    json=get_gs_coverage_body(layer['layer']['name'], band_name),
                    auth=HTTPBasicAuth(username, password),
                    headers=headers
                )
                print(f"Updated band name of layer '{layer['layer']['name']}' to '{band_name}'")
        except Exception as err:
            logger.error(err)


if __name__ == "__main__":
    # ----- Settings -----
    # GeoServer settings
    url = ""  # protected GeoServer url (layers shouldn't be public!)
    user = ""
    pw = ""
    convert_nc_to_geotiff = False  # convert NetCDF to GeoTIFF
    upload_layers = False  # upload layers to GeoServer
    update_styles = False  # update styles
    update_band_names = False  # update layer band names from GRAY_INDEX to something meaningful
    # Path to the folder which contains the NetCDF files
    base_path = "HRB_Eicherscheid_base_breach_scenario_IWD339m_HQ100_flowcorrected_roughinterp_alpha0.4_theta0.85"
    # New file name. The configured pattern will be extended with vel_* or wd_*, respectively.
    new_file_pattern = "hrb_eicherscheid_"

    # ----- Code -----
    if upload_layers or convert_nc_to_geotiff:
        logger.info(f"Start uploading dam break scenario data to GeoServer from {base_path}")
        files = os.listdir(base_path)
        geotiff_folder = os.path.join(base_path, "geotiff")
        if not os.path.exists(geotiff_folder):
            os.makedirs(geotiff_folder)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext == ".nc" or ext == ".netcdf":
                file_out = rename_file(file, new_file_pattern)
                if file_out is None:
                    continue
                file_out_full = os.path.join(geotiff_folder, file_out)
                if os.path.exists(file_out_full):
                    logger.info(f"File {file_out_full} already exists. Skipping conversion...")
                else:
                    logger.info(f"Convert {file} to {file_out}")
                    netcdf_to_geotiff(
                        os.path.join(base_path, file),
                        file_out_full,
                        25832,
                        3857
                    )
                if upload_layers:
                    upload_coverage_to_geoserver(file_out_full, url, user, pw)

    if update_styles:
        logger.info("Start updating layer styles in GeoServer")
        update_gs_styles(url, user, pw)
    if update_band_names:
        logger.info("Start updating layer band names in GeoServer")
        update_gs_band_names(url, user, pw)
