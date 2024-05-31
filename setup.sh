#!/usr/bin/env bash

# make sure that the code executes from the script's directory
# see: https://stackoverflow.com/a/29710607/16343968
cd -- "$(dirname "$BASH_SOURCE")"

python3 -m pip install -r requirements.txt || python -m pip install -r requirements.txt