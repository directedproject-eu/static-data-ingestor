# Project: DIRECTED
# Real World Lab: Danube Region
# Data:
# - Short description: ABSOLUT model crop data of the Danube basin
# - Original format: csv
#       Original files (each archive includes 12 csv files) received at 2025-11-06:
#       - danube_crop_yields_ssp126.zip
#       - danube_crop_yields_ssp370.zip
#       - danube_crop_yields_ssp585.zip
# The script restructures the data and optionally uploads them to the configured S3 bucket.
# The archives need to be unzipped before the script runs.
# The data does not contain any coordinates but only references to the NUTS regions.
# A separate file "danube_basin_territorial_units.geojson" contains Polygons for these NUTS regions.
# The NUTS region data can be downloaded from https://ec.europa.eu/eurostat/web/gisco/geodata/statistical-units/territorial-units-statistics.
import os
from pathlib import Path

import pandas as pd
from s3fs import S3FileSystem

# Necessary to avoid writing checksums into the files when uploading them to the bucket (cf. https://github.com/boto/boto3/issues/4435)
os.environ["AWS_REQUEST_CHECKSUM_CALCULATION"] = "when_required"
os.environ["AWS_RESPONSE_CHECKSUM_VALIDATION"] = "when_required"


def upload_to_bucket(local_path: str, bucket_path: str, endpoint: str, key: str, secret: str):
    print(f"Try to upload {local_path} to {bucket_path}")
    s3 = S3FileSystem(
        key=key,
        secret=secret,
        endpoint_url=endpoint
    )
    with open(local_path, 'rb') as local_file:
        with s3.open(bucket_path, 'wb') as s3_file:
            s3_file.write(local_file.read())
            print("Upload succeeded")


def restructure_and_upload_crop_data(
        input_base_path: str,
        output_base_path: str,
        bucket_base_path: str = None,
        endpoint: str = None,
        key: str = None,
        secret: str = None,
        upload: bool = False
):
    input_dir = Path(input_base_path)
    output_dir = Path(output_base_path)

    output_dir.mkdir(parents=True, exist_ok=True)

    for scenario_folder in input_dir.iterdir():
        if not scenario_folder.is_dir() or not scenario_folder.name.startswith("danube_crop_yields_"):
            continue

        scenario_name = scenario_folder.name.split("_")[-1].upper()
        print(f"Processing scenario: {scenario_name}...")

        for file_path in scenario_folder.glob("*.csv"):
            crop_name = file_path.name.split("_")[1]

            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error reading {file_path.name}: {e}")
                continue

            if 'NUTS' not in df.columns:
                print(f"Warning: 'NUTS' column not found in {file_path.name}. Skipping.")
                continue

            for region, region_df in df.groupby('NUTS'):
                target_dir = output_dir / str(region) / scenario_name
                target_dir.mkdir(parents=True, exist_ok=True)

                output_file = target_dir / f"{crop_name}.csv"
                region_df.to_csv(output_file, index=False)

                if upload:
                    bucket_path = f"{bucket_base_path}/{str(region)}/{scenario_name}/{os.path.basename(output_file)}"
                    upload_to_bucket(output_file, bucket_path, endpoint, key, secret)

    print("Restructuring complete!")


if __name__ == "__main__":
    INPUT_PATH = ""
    OUTPUT_PATH = "./restructured_data"

    upload = False
    bucket_endpoint = ""
    bucket_key = ""
    bucket_secret = ""
    bucket_name = ""
    bucket_base_path = f"{bucket_name}/data/crop_yield"

    restructure_and_upload_crop_data(
        INPUT_PATH, OUTPUT_PATH, bucket_base_path, bucket_endpoint, bucket_key, bucket_secret, upload
    )
