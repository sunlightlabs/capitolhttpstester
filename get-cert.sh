#!/bin/bash
# a lazy me ways to get a cert
# $1 -- hostname of cert to check
# $2 -- file name of cert to save

if [ -z $1 ]; then
    echo "need a hostname"
    exit 1
fi

if [ -z $2 ]; then
    echo "need a filename"
    exit 1
fi


echo -n | openssl s_client -connect $1:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > $2 
openssl x509 -text -in $2
