#!/bin/bash

set -u

sudo apt install -y gcc git python3 python3-setuptools python3-dev zlib1g-dev make zip libssl-dev libbz2-dev liblzma-dev libcurl4-openssl-dev build-essential

if [ ! -d "pynnotator" ]; then
  git clone https://github.com/raonyguimaraes/pynnotator
fi

cd pynnotator
python3 setup.py develop
pynnotator install
pynnotator test
