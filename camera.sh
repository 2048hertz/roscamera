#!/bin/bash

# Function to capture a picture
function take_picture() {
  local filename=$(date +"%Y-%m-%d_%H-%M-%S.jpg")
  rpicam-still -o "$HOME/Pictures/$filename" -t 5000  # Adjust -t for capture time in milliseconds
  zenity --info --text "Picture captured: $filename"
}

# Function to start recording a video
function start_recording() {
  local filename=$(date +"%Y-%m-%d_%H-%M-%S.h264")
  zenity --info --text "Recording started. Press any key to stop." &
  RECORD_PID=$!  # Store background process ID (Zenity)
  rpicam-vid -o "/tmp/$filename"  # Record to temporary file 

  # Wait for user to press any key (Zenity exits)
  wait $RECORD_PID

  # Stop recording and move file to Videos directory
  pkill -INT raspivid  # Send SIGINT signal to stop raspivid
  mv "/tmp/$filename" "$HOME/Videos/$filename"
  zenity --info --text "Recording stopped. Video saved: $filename"
}

# Main script body
zenity --question --text "Camera App" --ok-label="Take Picture" --cancel-label="Start Recording" --width=300 --height=100

# Check user selection ( $? holds exit code of zenity )
if [ $? -eq 0 ]; then
  take_picture
else
  start_recording
fi

exit 0
