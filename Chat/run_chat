#!/bin/bash

input_text="$1"
script="model_chat.py"

cd Chat/

if [[ -f "$script" ]]; then
    python3 "$script" --chat "$input_text"
else
    echo "Error $script is not found."
    exit
fi 

cd ..