#!/bin/bash

input_text="$1"
script="run_ask.py"

cd features/Ask/

if [[ -f "$script" ]]; then
    python3 "$script" --ask "$input_text"
else
    echo "Error $script is not found."
    exit
fi 

cd ..