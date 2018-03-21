#!/bin/bash

## This is handy as a boot-once script in Outset if you want software to be installed by default, but you don't want it to be managed.
## So users can see it installed, but if they want to uninstall the software later using Managed Software Center, they can.
## I put in a few example values in the optionalDefaults array. Feel free to tweak for your organization as you desire.

# Self-serve manifest location
manifestLocation='/Library/Managed Installs/manifests/SelfServeManifest'

# PlistBuddy full path
plistBuddy='/usr/libexec/PlistBuddy'

# Add in "optional" default software
optionalDefaults=("Firefox"
"GoogleChrome"
"MSExcel2016"
"MSWord2016"
"MSPowerPoint2016")

# Check to see if the file exists. If it doesn't, you may have to create it with an empty array; otherwise, 
if [ ! -f "$manifestLocation" ]; then
   "$plistBuddy" -c "Add :managed_installs array" "$manifestLocation"
fi

for packageName in "${optionalDefaults[@]}"
   do
      # Check it's not already in there
      alreadyExists=$("$plistBuddy" -c "Print: managed_installs" "$manifestLocation" | /usr/bin/grep "$packageName")

      # Single quote expansion of variables gets messy in bash, so we're going to pre-double-quote the single-quotes on the package name
      alteredPackageName="'""$packageName""'"
   
      if [ -z "$alreadyExists" ]; then
         "$plistBuddy" -c "Add :managed_installs: string $alteredPackageName" "$manifestLocation"
      fi
   done
