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
  python generate.py --i /home/varun/Dropbox/Public/Wiki --o output/ -r /
  cp static/* output/

  echo "Waiting for changes..."
  inotifywait -e modify -r /home/varun/Dropbox/Public/Wiki
done
