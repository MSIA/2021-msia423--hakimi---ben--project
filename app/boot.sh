#!/usr/bin/env bash

python3 run.py createDB
python3 run.py loadData 2021-msia423-hakimi-ben rawCSVUpload/raw.csv
python3 cleanData
python3 model
python3 app.py