#!/bin/bash

log_file="logs/hereiz.logs"

log() {
    local log_level="$1"
    local log_message="$2"
    echo "$(date +"%Y-%m-%d %H:%M:%S") [$log_level] - $log_message" >> "$log_file"
}

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [log_level] [log_message]"
    exit 1
fi

log "$1" "$2"
