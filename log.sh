#!/bin/bash

log_file="logs/hereiz.logs"

log() {
    local log_level="$1"
    local log_message="$2"
    local script_name="$3"
    local exit_status="$4"

    echo "$(date +"%Y-%m-%d %H:%M:%S") [SCRIPT: $script_name] [$log_level] - $log_message | Exit Status: $exit_status" >> "$log_file"
}

if [ "$#" -lt 3 ]; then
    echo "Usage: $0 [log_level] [log_message] [script_name] [exit_status]"
    exit 1
fi

log "$1" "$2" "$3" "$4" 
