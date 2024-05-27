#!/bin/bash

template_list=false
template_show=false

input_text=""

cd templates/

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -t)
            template_show=true
            shift
            input_text="$1"
            ;;
        -tl)
            template_list=true
            shift
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
    shift
done


if $template_show; then
    if [[ -f "$input_text" ]]; then
        cat "$input_text"
    elif [[ -f $input_text.txt ]]; then
        cat "$input_text.txt"
    else
        echo "No such template file: $input_text or $input_text.txt"
        echo "Check all the templates you have by running hereiz -tl"
        exit 1
    fi

elif $template_list; then
    ls *.txt

fi

exit