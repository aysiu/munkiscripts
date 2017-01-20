#!/bin/bash

# Use new cert after a certain date

# Define name of old one
old_cert='NAMEOFOLDCERT.pem'

# Define name of new one
new_cert='NAMEOFNEWCERT.pem'

# Define cert directory
cert_dir="/Library/Managed Installs/certs"

# Set timestamp threshold at which point we'll make the switch. This is the UNIX timestamp of the date/time.
threshold_timestamp=1485388800 # Pick a timestamp that makes sense for your org... this is just an example

# See what today's date is
current_timestamp=$(date +"%s")

# Check that the current timestamp is after the threshold timestamp and that both cert files exist
if [ "$current_timestamp" -gt "$threshold_timestamp" ] && [ -f "$cert_dir/$old_cert" ] && [ -f "$cert_dir/$new_cert" ]; then

    # Write the path to the new cert
    sudo defaults write /var/root/Library/Preferences/ManagedInstalls SoftwareRepoCACertificate "/Library/Managed Installs/certs/$new_cert"

fi
