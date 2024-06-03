#!/bin/bash

search_history_file="search_history.txt"

cd ../../../data/history/search/

if [ -f "$search_history_file" ]; then
    echo "The search history and responses : "
    cat "$search_history_file"
    echo " " 
else 
    echo "Can't fine the history file $search_history_file"
    echo "check the data/history/search/ to see if the file is found or no"
    exit 1
fi

exit