#!/usr/bin/env bash

# make sure that the code executes from the script's directory
# see: https://stackoverflow.com/a/29710607/16343968
cd -- "$(dirname "$BASH_SOURCE")"

python3 -m mystics_and_manuscripts.main || python -m mystics_and_manuscripts.main