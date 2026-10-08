# Project: DIRECTED
# Real World Lab: The Capital Region of Denmark
# Data:
# - Short description: coastal and pluvial flood simulations with RIM2D, SaferPlaces and Scalgo
# - Original format: NetCDF (RIM2D), GeoTIFF (SaferPlaces, Scalgo)
# - Original crs: EPSG:25832
# - New format: same as original
# - New crs: same as original (SaferPlaces, Scalgo), EPSG:4326 (RIM2D)
#   → reprojecting all files to the crs the frontend is using (typically EPSG:3857) might lead to a performance boost
# Detailed description:
# Model outputs from three models (RIM2D, SaferPlaces, Scalgo) were provided by DIRECTED project partners.
# In order to run this GeoServer upload script the files need to be provided in a specific structure:
# <base_folder>/<model_name>/<simulation_type>/<location>/<filename>
# See the variables "models", "simulation_types" and "locations" in the function "upload_new_data".
# The original files are renamed to have a clear and consistent layer naming in GeoServer.
# File naming scheme:
#   rwl1_<model>_<pluvial|coastal>_<location>_<value><unit>
# Examples:
#   rwl1_scalgo_pluvial_frederiksund_30mm
#   rwl1_saferplaces_coastal_jyllinge_170cm
# Note that special characters like æ might need be changed manually before running the script.
import os
import re

import xarray
from geo.Geoserver import Geoserver, GeoserverException


def rename_rim2d(name: str, simulation_type: str, location: str):
    free_flow = False
    if simulation_type == "pluvial":
        value= re.search('pluvial_(.*)mm', name).group(1)
        if value is None:
            raise RuntimeError()
        unit = "mm"
    elif simulation_type == "coastal":
        value = re.search('coastal_(.*)cm', name).group(1)
        if value is None:
            raise RuntimeError()
        if "free_flow" in name:
            free_flow = True
        unit = "cm"
    if free_flow:
        new_name = f"rwl1_rim2d_{simulation_type}_{location}_{value}{unit}_free_flow"
    else:
        new_name = f"rwl1_rim2d_{simulation_type}_{location}_{value}{unit}"
    return new_name


def rename_saferplaces(name: str, simulation_type: str, location: str):
    if simulation_type == "pluvial":
        value = re.search('RAIN_(.*).tif', name).group(1)
        if value is None:
            raise RuntimeError()
        unit = "mm"
    elif simulation_type == "coastal":
        try:
            value = re.search('COAST_(.*).tif', name).group(1)
        except AttributeError:
            value = re.search('Storm_(.*).tif', name).group(1)
        if value is None:
            raise RuntimeError()
        unit = "cm"
    else:
        raise RuntimeError()
    new_name = f"rwl1_saferplaces_{simulation_type}_{location}_{value}{unit}"
    return new_name


def rename_scalgo(name: str, simulation_type: str, location: str):
    if simulation_type == "pluvial":
        value_unit = re.search('=(.*).tif', name).group(1)
        if value_unit is None:
            raise RuntimeError()
        l = value_unit.split('_')
        # ['12', '0', 'cm'] or ['90', 'mm']
        value = l[0]
        unit = l[-1]
        if unit == "cm":
            value = f"{value}0"
            unit = "mm"
    elif simulation_type == "coastal":
        value_unit = re.search('_(.*).tif', name).group(1)  # '1.70m'
        if value_unit is None:
            raise RuntimeError()
        value = value_unit[:-1].replace(".", "")
        unit = "cm"
    else:
        raise RuntimeError()
    new_name = f"rwl1_scalgo_{simulation_type}_{location}_{value}{unit}"
    return new_name


def reproject(src_folder, destination_folder):
    filenames = os.listdir(src_folder)
    for filename in filenames:
        out = os.path.join(destination_folder, filename)
        if os.path.exists(out):
            print(f"{out} already exists. Skipping reprojection...")
        else:
            dataset = xarray.open_dataset(os.path.join(src_folder, filename))
            # Rename coordinates (not necessary for GeoServer)
            dataset = dataset.rename({'y': 'latitude'})
            dataset = dataset.rename({'x': 'longitude'})
            # Write crs to netcdf file
            dataset.rio.write_crs(25832, inplace=True)
            # Reproject to EPSG:4326
            dataset = dataset.rio.reproject('EPSG:4326')
            dataset.rio.write_crs(4326, inplace=True)
            # Write to file
            dataset.to_netcdf(out)


def name_generator(files: list, model: str, simulation_type: str, location: str):
    for file in files:
        if file.endswith(".tif") or file.endswith(".nc"):
            if model == "scalgo":
                yield file, rename_scalgo(file, simulation_type, location)
            elif model == "rim2d":
                yield file, rename_rim2d(file, simulation_type, location)
            elif model == "saferplaces":
                yield file, rename_saferplaces(file, simulation_type, location)


def upload_coverage_to_geoserver(
        filename: str,
        layer_name: str,
        url: str,
        username:str,
        password: str,
        workspace: str = 'directed',
        file_type: str = 'GeoTIFF',
        content_type: str = 'image/tiff',
        overwrite: bool = False
):
    client = Geoserver(url, username=username, password=password)
    # FIXME: layer title is still wrong
    exists = False
    try:
        client.get_layer(layer_name)
        exists = True
    except GeoserverException:
        pass
    if exists:
        if overwrite:
            print(f"Layer '{layer_name}' already exists and overwrite is True. Re-upload...")
            client.create_coveragestore(layer_name=layer_name, path=filename, workspace=workspace,
                                    file_type=file_type, content_type=content_type)
        else:
            print(f"Layer '{layer_name}' already exists and overwrite is False. Skipping...")
    else:
        client.create_coveragestore(layer_name=layer_name, path=filename, workspace=workspace,
                                    file_type=file_type, content_type=content_type)


def update_style(layer_name, url: str, username: str, password: str,
                 style_name: str = 'water_level_transparent', workspace: str = "directed"):
    client = Geoserver(url, username=username, password=password)
    try:
        layer = client.get_layer(layer_name)
        if layer['layer']['type'] == 'RASTER':
            client.publish_style(layer_name, style_name, workspace=workspace)
    except Exception as err:
        print(err)


def upload_new_data(base_path: str, gs_url: str, gs_user: str, gs_pw: str):
    models = ["rim2d", "saferplaces", "scalgo"]
    simulation_types = ["pluvial", "coastal"]
    locations = ["frederikssund", "frederiksvaerk", "halsnaes", "jyllinge", "roskilde", "roskilde_fjord"]

    counter = 0
    for model in models:
        model_path = os.path.join(base_path, model)
        for simulation_type in simulation_types:
            simulation_type_path = os.path.join(model_path, simulation_type)
            for location in locations:
                location_path = os.path.join(simulation_type_path, location)
                try:
                    files = os.listdir(location_path)
                except FileNotFoundError:
                    continue
                for file_orig, layer_name in name_generator(files, model, simulation_type, location):
                    print(f"Start uploading {file_orig} to GeoServer as {layer_name}")
                    if model == "rim2d":
                        upload_coverage_to_geoserver(
                            os.path.join(location_path, file_orig), layer_name, gs_url, gs_user, gs_pw,
                            file_type="NetCDF", content_type="application/x-netcdf")
                    else:
                        upload_coverage_to_geoserver(os.path.join(location_path, file_orig), layer_name,
                                                     gs_url, gs_user, gs_pw)
                    update_style(layer_name, gs_url, gs_user, gs_pw)
                    counter += 1
                    print(f"Upload successful")
    if counter != 246:
        raise RuntimeError(f"The expected number of layers was not uploaded! Actual: {counter}, expected: 225")


if __name__ == "__main__":
    url = ""  # GeoServer url
    user = ""
    pw = ""

    base_path = ""  # path to the base folder; this folder should contain 3 subfolders: rim2d, saferplaces, scalgo
    # optional reprojection (only NetCDF → RIM2D)
    # reproject(os.path.join(base_path, "rim2d/pluvial/roskilde_fjord/orig"),
    #           os.path.join(base_path, "rim2d/pluvial/roskilde_fjord"))
    # reproject(os.path.join(base_path, "rim2d/coastal/roskilde_fjord/orig"),
    #           os.path.join(base_path, "rim2d/coastal/roskilde_fjord"))
    upload_new_data(base_path, url, user, pw)
