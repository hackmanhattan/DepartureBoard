#!/bin/bash
mkdir deps
python3 -m venv deps
source ./deps/bin/activate
python3 -m pip install requests
