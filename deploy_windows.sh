#!/bin/sh

# Create site dir if it does not exist
mkdir -p output

echo "Building site..."
python generate.py --i "/c/Users/Varun/Dropbox/Public/Wiki" --outputdir "output\\" --root 'http://www.varunramesh.net/wiki/'
cp static/* output/

scp -C -r output/. root@varunramesh.net:/sites/varunramesh.net/public/wiki/