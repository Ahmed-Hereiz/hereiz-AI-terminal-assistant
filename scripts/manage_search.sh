#!/bin/bash

cd src/managment/manage_search/ || { echo "Error: Directory 'src/managment/manage_search/' not found."; exit 1; }

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -searchshow| --search_show)
            bash ./search_searchshow.sh 
            ;;
        -searchclr| --search_clear)
            bash ./search_searchclr.sh 
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
    shift
done
