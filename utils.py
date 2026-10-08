import logging
import os

import xarray
from geo.Geoserver import Geoserver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_coverage_to_geoserver(
        filename: str,
        url:str,
        username:str,
        password: str,
        workspace: str = 'directed',
        file_type: str = 'GeoTIFF',
        content_type: str = 'image/tiff'
):
    """
    :param filename: absolute path to the file that should be uploaded
    :param url: GeoServer base url
    :param username:
    :param password:
    :param workspace:
    :param file_type:
    :param content_type:
    :return:
    """
    client = Geoserver(url, username=username, password=password)
    temp = os.path.splitext(os.path.basename(filename))
    layer_name = temp[0]
    # Will overwrite layer if it exists
    # FIXME: layer title is still wrong
    client.create_coveragestore(layer_name=layer_name, path=filename, workspace=workspace,
                                file_type=file_type, content_type=content_type)
    logger.info(f"Uploaded {filename} to GeoServer")


def upload_shapefile_to_geoserver(
        filename: str,
        url: str,
        username: str,
        password: str,
        workspace: str = 'directed'
):
    """
    :param filename: absolute path to the file that should be uploaded
    :param url: GeoServer base url
    :param username:
    :param password:
    :param workspace:
    :return:
    """
    client = Geoserver(url, username=username, password=password)
    temp = os.path.splitext(os.path.basename(filename))
    store_name = temp[0]
    # Will overwrite layer if it exists
    client.create_shp_datastore(path=filename, store_name=store_name, workspace=workspace)
    logger.info(f"Uploaded {filename} to GeoServer")


def upload_geopackage_to_geoserver(
        filename: str,
        url: str,
        username: str,
        password: str,
        workspace: str = 'directed'
):
    """
    :param filename: absolute path to the file that should be uploaded
    :param url: GeoServer base url
    :param username:
    :param password:
    :param workspace:
    :return:
    """
    client = Geoserver(url, username=username, password=password)
    # client.create_workspace(workspace)
    temp = os.path.splitext(os.path.basename(filename))
    store_name = temp[0]
    # Will overwrite layer if it exists
    client.create_gpkg_datastore(path=filename, store_name=store_name, workspace=workspace)
    logger.info(f"Uploaded {filename} to GeoServer")


def update_style(
        style_name: str,
        layer_name: str,
        url: str,
        username: str,
        password: str,
        workspace: str = 'directed'
):
    """
    :param style_name: style name
    :param layer_name: layer name
    :param url: GeoServer base url
    :param username:
    :param password:
    :param workspace:
    :return:
    """
    try:
        client = Geoserver(url, username=username, password=password)
        client.publish_style(layer_name, style_name, workspace=workspace)
    except Exception as err:
        logger.error(err)


def netcdf_to_geotiff(input_file, output_file, from_crs=None, to_crs=None, driver="GTiff", creation_options=None):
    ds = xarray.open_dataset(input_file)
    if from_crs:
        ds = ds.rio.write_crs(from_crs)
    if to_crs:
        ds = ds.rio.reproject(to_crs)
    if creation_options is None:
        creation_options = {
            "compress": "deflate",
            "predictor": "3",
            'interleave': 'band',
            "tiled": "YES",
            "blockxsize": "512",
            "blockysize": "512",
            "num_threads": "ALL_CPUS"
        }
    ds.rio.to_raster(output_file, driver=driver, **creation_options)


def get_gs_coverage_body(layer_name: str, new_band_name: str, workspace: str = "directed"):
    return {
        "coverage": {
            "name": layer_name,
            "namespace": {
                "name": workspace
            },
            "dimensions": {
                "coverageDimension": {
                    "name": new_band_name
                }
            }
        }
    }
