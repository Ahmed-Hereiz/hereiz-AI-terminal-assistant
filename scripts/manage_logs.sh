#!/bin/bash

cd src/managment/manage_logs/ || { echo "Error: Directory 'src/managment/manage_logs/' not found."; exit 1; }

while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -viewlogs)
            bash ./logs_viewlogs.sh
            ;;
        -clrlogs)
            bash ./logs_clrlogs.sh
            ;;
        *)
            echo "Unknown option: $key"
            exit 1
            ;;
    esac
    shift
done

exit