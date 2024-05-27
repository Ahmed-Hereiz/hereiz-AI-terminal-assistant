#!/bin/bash

searchopen=false
search=false
sso=false
input_text=""

cd Search/

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
        -sso)
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
    script="model_search.py"
    if [[ -f "$script" ]]; then
        python3 "$script" --searchopen "$input_text"
        if [[ -f tmp_link ]]; then
            link=$(cat tmp_link)
            rm tmp_link
            google-chrome "$link"
        else
            echo "Error: tmp_link file created by $script was not created. Ensure the Python script ran successfully."
            exit 1
        fi
    else
        echo "Error: $script not found."
        exit 1
    fi

elif $search; then
    script="agent_search.py"
    if [[ -f "$script" ]]; then
        python3 "$script" --search "$input_text"
    else
        echo "Error: $script not found."
        exit 1
    fi

elif $sso; then
    script_open="model_search.py"
    script_search="agent_search.py"

    if [[ -f "$script_open" ]]; then
        python3 "$script_open" --searchopen "$input_text"
        if [[ -f tmp_link ]]; then
            link=$(cat tmp_link)
            rm tmp_link
            google-chrome "$link"
        else
            echo "Error: tmp_link file created by $script_open was not created. Ensure the Python script ran successfully."
            exit 1
        fi
        echo "in summary:"
        if [[ -f "$script_search" ]]; then
            python3 "$script_search" --search "$input_text"
        else
            echo "Error: $script_search not found."
            exit 1
        fi
    else
        echo "Error: $script_open not found."
        exit 1
    fi
else
    echo "No valid option provided."
    usage
    exit 1
fi

cd ..