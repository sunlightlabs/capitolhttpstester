#!/bin/bash

time ./virt/bin/python ./capitolhttpstester.py > out.json
./virt/bin/python ./maketable.py && s3cmd put tester-results.html --acl-public s3://sunlight-cdn/ssl-survey/
