#!/bin/bash

VARIABLES=("r010s_370" "r025s_370" "r050s_370" "r100s_370" "r250s_370" "r010s_585" "r025s_585" "r050s_585" "r100s_585" "r250s_585")
SOURCE_FILE="danube_flood_return_period_shifts.gpkg"
BASE_OUT_FOLDER="<my-base-folder>"
PREFIX="danube_flood_return_period_shifts"
VALUE_NAME="return_period"

for i in "${VARIABLES[@]}"
do
  filename_out="${BASE_OUT_FOLDER}/${PREFIX}_${i}.gpkg"
  echo "Extract attribute ${i} from ${SOURCE_FILE} and save new file: $filename_out"
  ogr2ogr -sql "SELECT geom,cat,STRAHLER,nameText,nameTxtInt,$i AS ${VALUE_NAME}  FROM danube_flood_return_period_shifts" -nln "${PREFIX}_${i}" ${filename_out} ${SOURCE_FILE}
done

