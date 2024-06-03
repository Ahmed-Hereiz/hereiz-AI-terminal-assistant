#!/bin/bash

logs_file="hereiz.logs"

cd ../../../logs/

rm "$logs_file"
touch "$logs_file"

echo "all logs cleared !"

exit