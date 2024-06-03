#!/bin/bash

input_text="$1"

cd ../../../data/history/memory/

if [ -f "$input_text" ]; then
    echo "The model memory : "
    cat "$input_text"
    echo " "
else
    echo "No such memory file: $input_text "
    echo "Check all the memories you have by running hereiz -memlst"
    exit 1
fi

exit