#!/bin/bash

show_memory=false
clear_memory=false
list_memory=false

input_text=""

cd data/history/

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -memshow| --memory_show)
            show_memory=true
            shift
            input_text="$1"
            ;;
        -memclr| --memory_clear)
            clear_memory=true
            shift
            input_text="$1"
            ;;
        -memlst| --memory_list)
            list_memory=true
            shift
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
    shift
done


if $show_memory; then
    if [ -f "$input_text" ]; then
        echo "The model memory : "
        cat "$input_text"
        echo " "
    else
        echo "No such memory file: $input_text "
        echo "Check all the memories you have by running hereiz -memlst"
        exit 1
    fi

elif $clear_memory; then
    if [ -f "$input_text" ]; then
        rm "$input_text"
        touch "$input_text"
        echo "memroy cleared"
    else
        echo "No such memory file: $input_text "
        echo "Check all the memories you have by running hereiz -memlst"
        exit 1
    fi

elif $list_memory; then
    ls

    
fi

exit
