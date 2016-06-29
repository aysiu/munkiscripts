#!/bin/bash

## This is a preinstall_script for a pkginfo file to not install the item unless a user is logged in.
## Warning: Absolutely be sure that you don't make this a preinstall_script for an item that requires a logout or reboot in order to install!!!

# Get the state of the lastuser
lastUser=$(defaults read /Library/Preferences/com.apple.loginwindow.plist lastUser)

# Check if the last user is logged in...
if [ ! -z "$lastUser" ] && [ "$lastUser" == "loggedIn" ]; then

  # If the last user is logged in, proceed...
  exit 0
   
else
  
  # Otherwise abort installing this item
   exit 1
   
fi
