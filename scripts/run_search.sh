#!/bin/bash

searchopen=false
search=false
sso=false
input_text=""

cd src/features/ || { echo "Error: Directory 'src/features/' not found."; exit 1; }

tmp_link=../../data/tmp/tmp_link

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --searchopen|-so)
            searchopen=true
            shift
            input_text="$1"
            ;;
        --search|-s)
            search=true
            shift
            input_text="$1"
            ;;
        --fullsearch|-sso)
            sso=true
            shift
            input_text="$1"
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
    shift
done

if $searchopen; then
    python3 Search/ -so "$input_text"
    if [[ -f "$tmp_link" ]]; then
        link=$(cat "$tmp_link")
        rm "$tmp_link"
        google-chrome "$link"
    else
        echo "Error: tmp_link file was not created. Ensure the Python script ran successfully."
        exit 1
    fi

elif $search; then
    python3 Search/ -s "$input_text"
    

elif $sso; then
    python3 Search/ -sso "$input_text"
    if [[ -f "$tmp_link" ]]; then
        link=$(cat "$tmp_link")
        rm "$tmp_link"
        google-chrome "$link"
    else
        echo "Error: tmp_link file created by $script_open was not created. Ensure the Python script ran successfully."
        exit 1
    fi

else
    echo "No valid option provided."
    usage
    exit 1
fi

exit