#!/bin/bash

input_text="$1"

cd ../../../templates/

if [[ -f "$input_text" ]]; then
    cat "$input_text"
elif [[ -f $input_text.txt ]]; then
    cat "$input_text.txt"
else
    echo "No such template file: $input_text or $input_text.txt"
    echo "Check all the templates you have by running hereiz -tl"
    exit 1
fi

exit
