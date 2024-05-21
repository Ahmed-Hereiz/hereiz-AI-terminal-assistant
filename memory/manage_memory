#!/bin/bash

show_memory=false
clear_memory=false


cd memory/

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -memshow| --memory_show)
            show_memory=true
            shift
            ;;
        -memclr| --memory_clear)
            clear_memory=true
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
    if [ -f memory_buffer ]; then
        echo "The model memory : "
        cat memory_buffer
        echo " "
    else
        echo "Something wrong there is no memory buffer file"
        exit 1
    fi

elif $clear_memory; then
    rm -f memory_buffer
    touch memory_buffer

echo "memroy cleared"

fi

cd ..
