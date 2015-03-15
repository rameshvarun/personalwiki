#!/bin/sh

# Create site dir if it does not exist
mkdir -p output

# Python server
cd output
python -m SimpleHTTPServer 3000 &
cd ..

# Kill python server on exit
trap "exit" INT TERM
trap "kill 0" EXIT

while true; do
  echo "Building site..."
  python generate.py --i "C:\Users\Varun Ramesh\Dropbox\Public\Wiki" --outputdir "output\\" --root 'http://localhost:3000/'
  cp static/* output/

  echo "Waiting for changes..."
  read -p "Press any key to rebuild... " -n1 -s
done
