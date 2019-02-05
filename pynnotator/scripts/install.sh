#!/bin/bash

set -u

sudo apt-get install gcc git python3-dev zlib1g-dev make zip libssl-dev libbz2-dev liblzma-dev libcurl4-openssl-dev build-essential

git clone https://github.com/raonyguimaraes/pynnotator
cd pynnotator
python setup.py develop
