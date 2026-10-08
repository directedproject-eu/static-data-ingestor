# Project: DIRECTED
# Real World Lab: Danube Region
# Data:
# - Short description: ISIMIP climate projections upload to an S3 bucket
# - Original format: NetCDF
# - Original crs: EPSG:4326
# - New format: COG
# - New crs: same as original
# Detailed description:
#
# Steps:
# 1) Convert original NetCDFs to TIFs
# 2) Convert TIFs to COGs
# 3) Convert COGs to single bands (one file per month per year)
# 4) Upload single-band COGs to OTC bucket
#
# Folder structure after transformation from NetCDF to COG:
# cogs
#   - ssp370
#      - canesm5
#         - hurs
#            - 1320 tif files (e.g. ssp370_canesm5_hurs_mon_1991-1.tif) from 1991-1 to 2100-12
#         - ... [all variables]
#      - ... [all models]
#   - ssp585
#      - canesm5
#      - ... [all models]


import os
import subprocess

from osgeo import gdal
from s3fs import S3FileSystem

# Necessary to avoid writing checksums into the COGs when uploading them to the bucket (cf. https://github.com/boto/boto3/issues/4435)
os.environ["AWS_REQUEST_CHECKSUM_CALCULATION"] = "when_required"
os.environ["AWS_RESPONSE_CHECKSUM_VALIDATION"] = "when_required"

scenarios = ["ssp370", "ssp585"]
models = ["canesm5", "cnrm-cm6-1", "cnrm-esm2-1", "ec-earth3", "gfdl-esm4",
          "ipsl-cm6a-lr", "miroc6", "mpi-esm1-2-hr", "mri-esm2-0", "ukesm1-0-ll"]
variables = ["hurs", "pr", "rsds", "sfcwind", "tasmax", "tasmin", "tas", "spei12"]


def netcdf_to_geotiff(netcdf_file, subdataset, output_file):
    subdataset_path = f"NETCDF:\"{netcdf_file}\":{subdataset}"
    subprocess.run(["gdal_translate", subdataset_path, output_file])

def geotiff_to_cog(input_file, output_file):
    subprocess.run([
        "gdal_translate", "-of", "COG", "-co", "COMPRESS=LZW", "-a_srs",  "EPSG:4326", input_file, output_file
    ])

def transform_cog_to_single_bands_and_upload_to_bucket(cog_file, folder_name, bucket_path=None, key=None, secret=None, upload=False):
    dataset = gdal.Open(cog_file)
    for year in range(1991, 2101): 
        for month in range(1, 13):
            output_file = os.path.join(folder_name, os.path.splitext(os.path.basename(cog_file))[0] + "_" + str(year) + "-" + str(month) + ".tif")
            if not os.path.isfile(output_file):
                band = str((year - 1991)*12 + month)
                gdal.Translate(output_file, dataset, bandList=[band], options=["BIGTIFF=YES"])
            if upload:
                upload_to_bucket(output_file, bucket_path+os.path.basename(output_file), key, secret)

dataset = None  # Close dataset

def upload_to_bucket(local_path, bucket_path, key, secret):
    print(f"Try to upload {local_path} to {bucket_path}")
    s3 = S3FileSystem(
        key=key,
        secret=secret,
        endpoint_url=""
    )
    with open(local_path, 'rb') as local_file:
        with s3.open(bucket_path, 'wb') as s3_file:
            s3_file.write(local_file.read())
            print("Upload succeeded")


if __name__ == "__main__":
    base_dir_netcdf = "<directory>"
    base_dir_cog = os.path.join(os.getcwd(), "cogs")
    upload = False
    bucket_key = "<key>"
    bucket_secret = "<secret>"
    bucket_name = "<bucket>"
    bucket_base_path = "data/isimip"
    if not os.path.exists(base_dir_cog):
        os.makedirs(base_dir_cog)
    for scenario in scenarios: 
        current_folder = os.path.join(base_dir_cog, scenario)
        if not os.path.exists(current_folder):
            os.makedirs(current_folder)
        for model in models:
            current_folder = os.path.join(base_dir_cog, scenario, model)
            if not os.path.exists(current_folder):
                os.makedirs(current_folder)
            for variable in variables: 
                current_folder = os.path.join(base_dir_cog, scenario, model, variable)
                if not os.path.exists(current_folder):
                    os.makedirs(current_folder)
                nc_subfolder = scenario + "_" + variable + "_mon"
                nc_filename = scenario + "_" + model + "_" + variable  + "_mon.nc"
                INPUT_FILE = os.path.join(base_dir_netcdf, nc_subfolder, nc_filename)
                OUTPUT_COG = os.path.join(current_folder, scenario + "_" + model + "_" + variable + "_mon.tif")
                SUBDATASET = variable
                if variable == "spei12":
                    SUBDATASET = "spei"
                temp_tif_file = os.path.join(base_dir_cog, "temp.tif")
                netcdf_to_geotiff(INPUT_FILE, SUBDATASET, temp_tif_file)
                geotiff_to_cog(temp_tif_file, OUTPUT_COG)
                os.remove(temp_tif_file)
                cog_bucket_path = f"{bucket_name}/{bucket_base_path}/cogs/{scenario}/{model}/{variable}/"
                transform_cog_to_single_bands_and_upload_to_bucket(OUTPUT_COG, current_folder, cog_bucket_path, bucket_key, bucket_secret, upload)
                os.remove(OUTPUT_COG)
                if os.path.isfile(OUTPUT_COG + ".aux.xml"):
                    os.remove(OUTPUT_COG + ".aux.xml")
