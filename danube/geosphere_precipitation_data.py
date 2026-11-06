# Project: DIRECTED
# Real World Lab: Danube Region
# Data:
# - Short description: daily precipitation sums for 2024 around Vienna downloaded from GeoSphere Austria
# - Original format: NetCDF
# - Original crs: EPSG:3416 - ETRS89 / Austria Lambert
# - New crs: EPSG:4326
#   → reprojecting all files to the crs the frontend is using (typically EPSG:3857) might lead to a performance boost
# The original NetCDF file contains 366 time stamps from 2024-01-01 to 2024-12-31.
# The script splits the NetCDF file into time slices, transforms them to COG, and optionally uploads them to a bucket.
import logging
import os
import sys

import pyproj
import xarray
from osgeo import gdal
from s3fs import S3FileSystem

# Necessary to avoid writing checksums into the COGs when uploading them to the bucket (cf. https://github.com/boto/boto3/issues/4435)
os.environ["AWS_REQUEST_CHECKSUM_CALCULATION"] = "when_required"
os.environ["AWS_RESPONSE_CHECKSUM_VALIDATION"] = "when_required"

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


def netcdf_to_cog(input_file, output_file):
    dataset = gdal.Open(input_file)
    options = gdal.TranslateOptions(format="COG", creationOptions=["COMPRESS=LZW"], outputSRS="EPSG:4326")
    gdal.Translate(output_file, dataset, options=options)
    dataset = None


def reproject_from_lambert(xarray_dataset, crs_to="epsg:4326"):
    crs_from = pyproj.CRS.from_epsg(3416)  # EPSG:3416 - ETRS89 / Austria Lambert
    xarray_dataset.rio.write_crs(crs_from, inplace=True)
    xarray_dataset = xarray_dataset.rio.reproject(crs_to)
    return xarray_dataset


def transform_cog_to_single_bands_and_upload_to_bucket(
        cog_file, folder_name, times, bucket_name=None, bucket_path=None, endpoint=None,
        key=None, secret=None, upload=False
):
    dataset = gdal.Open(cog_file)
    for band, t in enumerate(times):
        time_str = str(t).split('.')[0].replace("-", "").replace(":", "")
        output_file = os.path.join(folder_name, time_str + ".tif")
        gdal.Translate(output_file, dataset, bandList=[band+1], options=["BIGTIFF=YES"])
        if upload:
            upload_to_bucket(output_file, f"{bucket_name}/{bucket_path}/{os.path.basename(output_file)}",
                             endpoint, key, secret)
            if band % 10 == 0:
                logger.info(f"Uploaded {band} of {len(times)} files.")
    dataset = None


def upload_to_bucket(local_file, bucket_file, endpoint_url, key, secret):
    logger.debug(f"Try to upload {local_file} to {bucket_file}.")
    s3 = S3FileSystem(
        endpoint_url=endpoint_url,
        key=key,
        secret=secret
    )
    with open(local_file, 'rb') as f:
        with s3.open(bucket_file, 'wb') as s3_file:
            s3_file.write(f.read())
            logger.debug("Upload succeeded.")


if __name__ == "__main__":
    logger.info("Start upload script for weather data from GeoSphere.")
    # Configurable parameters
    bucket_endpoint = ""
    bucket_name = ""
    bucket_path = "data/geosphere/historical/daily_precipitation_sum"
    bucket_key = ""
    bucket_secret = ""
    upload = False
    # Fixed parameters
    base_data_dir = ""  # needs to be set!
    nc_filename_orig = "SPARTACUS2-DAILY_RR_2024.nc"
    nc_filename = os.path.join(base_data_dir, "temp.nc")
    cog_filename = os.path.join(base_data_dir, "temp.tif")

    if not os.path.exists(base_data_dir):
        os.makedirs(base_data_dir)

    logger.info(f"Reproject data.")
    ds = xarray.open_dataset(nc_filename_orig)
    ds = reproject_from_lambert(ds)
    logger.info(f"Save reprojected data to NetCDF.")
    ds.to_netcdf(nc_filename)
    logger.info(f"Transform NetCDF to COG.")
    netcdf_to_cog(nc_filename, cog_filename)
    logger.info(f"Split COG into bands (time slices) and upload them to bucket.")
    transform_cog_to_single_bands_and_upload_to_bucket(
        cog_filename, base_data_dir, ds.time.values, bucket_name, bucket_path, bucket_endpoint, bucket_key,
        bucket_secret, upload)
    try:
        os.remove(nc_filename)
        os.remove(cog_filename)
    except Exception as err:
        logger.warning(err)
