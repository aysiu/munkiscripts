#!/bin/bash

## This is handy as a boot-once script in Outset if you want software to be installed by default, but you don't want it to be managed.
## So users can see it installed, but if they want to uninstall the software later using Managed Software Center, they can.
## I put in a few example values in the optionalDefaults array. Feel free to tweak for your organization as you desire.

# Add in "optional" default software
optionalDefaults=("Firefox"
"GoogleChrome"
"MSExcel2016"
"MSWord2016"
"MSPowerPoint2016")

for packageName in "${optionalDefaults[@]}"
do
# Check it's not already in there
   alreadyExists=$(/usr/libexec/PlistBuddy -c "Print: managed_installs" /Library/Managed\ Installs/manifests/SelfServeManifest | grep "$packageName")

   # Single quote expansion of variables gets messy in bash, so we're going to pre-double-quote the single-quotes on the package name
   alteredPackageName="'""$packageName""'"
   
   # Add only if it doesn't already exist
   if [ -z "$alreadyExists" ]; then
      sudo /usr/libexec/PlistBuddy -c "Add :managed_installs:0 string $alteredPackageName" /Library/Managed\ Installs/manifests/SelfServeManifest
   fi
done
