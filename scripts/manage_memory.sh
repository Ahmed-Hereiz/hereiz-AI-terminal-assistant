#!/bin/bash

input_text=""

cd src/managment/manage_memory/ || { echo "Error: Directory 'src/managment/manage_memory/' not found."; exit 1; }

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -memshow| --memory_show)
            shift
            input_text="$1"
            bash ./memory_memshow.sh "$1"
            ;;
        -memclr| --memory_clear)
            shift
            input_text="$1"
            bash ./memory_memclr.sh "$1"
            ;;
        -memlst| --memory_list)
            bash ./memory_memlst.sh
            shift
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
    shift
done
