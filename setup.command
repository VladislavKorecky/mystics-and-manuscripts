#!/usr/bin/env bash

# make sure that the code executes from the script's directory
# see: https://stackoverflow.com/a/29710607/16343968
cd -- "$(dirname "$BASH_SOURCE")"

pip3 install -r requirements.txt || pip install -r requirements.txt