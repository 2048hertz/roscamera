#!/bin/bash

# Path to the Python script
BASH_SCRIPT="/usr/bin/RobertOS-assets/roscamera-main/camera.sh"

# Name of the desktop file
DESKTOP_FILE="/usr/share/applications/Robert_Camera_App.desktop"

# Create the .desktop file
cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Exec=bash "/usr/bin/RobertOS-assets/roscamera-main/camera.sh"
Name=Camera
Comment=Camera application for the Robert computer
Icon=/usr/bin/RobertOS-assets/roscamera.png
Categories=Utility;
EOF

# Make the .desktop file executable
chmod +x "$DESKTOP_FILE"

echo "Desktop file created at: $DESKTOP_FILE"
