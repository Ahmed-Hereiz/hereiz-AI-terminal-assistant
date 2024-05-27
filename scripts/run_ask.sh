#!/bin/bash

input_text="$1"

if [[ -z "$input_text" ]]; then
    echo "Usage: ./hereiz -a 'your question here'"
    exit 1
fi

cd src/features/ || { echo "Error: Directory 'src/features/' not found."; exit 1; }

python3 Ask/ -a "$input_text"

exit