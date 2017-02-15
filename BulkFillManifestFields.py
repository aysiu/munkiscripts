#!/usr/bin/python

####
## A one-off script written just for my setup, but I thought others might find it useful... very rudimentary
####

import os
import plistlib

# Obviously modify this to be the actual path to your repo... could be /var/www/html/munki_repo/manifests, for example
manifest_dir='/Library/WebServer/Documents/munki_repo/manifests'

# Dictionary of manifest names by serial number and then their desired computer names
serial_name={ 'SERIALNUMBERONE': 'DESIREDCOMPUTERNAMEONE', 'SERIALNUMBERTWO': 'DESIREDCOMPUTERNAMETWO', 'SERIALNUMBERTHREE': 'DESIREDCOMPUTERNAMETHREE', 'SERIALNUMBERFOUR': 'DESIREDCOMPUTERNAMEFOUR' }

# Loop through dictionary
for serial,name in serial_name.items():

    # Get the full path to the serial number based on the manifest dir. I don't have subfolders, but if you do, you'd probably want to modify this to do an os.walk() instead
    full_path=os.path.join(manifest_dir,serial)
    
    # Double-check the path is an actual file
    if os.path.isfile(full_path):

        # Read the current plist
        plist=plistlib.readPlist(full_path)

        # Change display name (or notes or user) to desired name
        plist['display_name']=name
        #plist['notes']=name
        #plist['user']=name

        # Write back the plist
        plistlib.writePlist(plist,full_path)
