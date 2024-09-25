#!/bin/bash

Y_TOLERANCE=30

if [ -z "$1" ]; then
  echo "Usage: $0 --screen_shot_dir <directory>"
  exit 1
fi

screenshot_dir="$1"

if [ ! -d "$screenshot_dir" ]; then
  echo "Directory $screenshot_dir does not exist. Creating it..."
  mkdir -p "$screenshot_dir"
fi

screenshot_file="$screenshot_dir/screenshot.png"

active_window_id=$(xprop -root _NET_ACTIVE_WINDOW | awk -F' ' '{print $5}')
if [ -z "$active_window_id" ]; then
  echo "Could not get the active window ID."
  exit 1
fi

window_info=$(xwininfo -id "$active_window_id")
if [ -z "$window_info" ]; then
  echo "Could not retrieve window information."
  exit 1
fi

x=$(echo "$window_info" | grep "Absolute upper-left X" | awk '{print $4}')
y=$(echo "$window_info" | grep "Absolute upper-left Y" | awk '{print $4}')

screens=$(xrandr --listmonitors | tail -n +2)

selected_screen=""
screen_x=""
screen_y=""
screen_width=""
screen_height=""

while IFS= read -r line; do
  screen_name=$(echo "$line" | awk '{print $4}')
  resolution=$(echo "$line" | awk '{print $3}' | cut -d'/' -f1)
  screen_x=$(echo "$line" | awk '{print $3}' | cut -d'+' -f2)
  screen_y=$(echo "$line" | awk '{print $3}' | cut -d'+' -f3)
  screen_width=$(echo "$resolution" | cut -d'x' -f1)
  screen_height=$(echo "$resolution" | cut -d'x' -f2)

  if [ "$x" -ge "$screen_x" ] && [ "$x" -lt $(($screen_x + $screen_width)) ] &&
     [ "$y" -ge $(($screen_y - $Y_TOLERANCE)) ] && [ "$y" -lt $(($screen_y + $screen_height)) ]; then
    selected_screen="$screen_name"
    break
  fi
done <<< "$screens"

if [ -z "$selected_screen" ]; then
  echo "Could not determine which screen the terminal is on."
  exit 1
fi

if [ -f "$screenshot_file" ]; then
  rm "$screenshot_file"
fi

scrot -a "$screen_x,$screen_y,$screen_width,$screen_height" "$screenshot_file"

exit
