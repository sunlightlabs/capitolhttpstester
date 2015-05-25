#!/bin/bash

virtualenv --no-site-packages virt
source virt/bin/activate
./virt/bin/pip install -r requirements.txt
