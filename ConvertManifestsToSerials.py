#!/usr/bin/python

#### This script will copy/convert named manifests to serial number manifests
#### This isn't meant out of the box to work on any Munki repository. This is just something I (aysiu) created that I found useful in its current form for my organization, but that I also thought others could adapt for their own needs... so read it over carefully, and make adjustments as fits your own organization's needs.
#### Also keep in mind this does nothing to included manifests that shouldn't have a serial number, so you'll probably want to migrate those over later without modification.

import os
import shutil
import subprocess

## Define the source manifests directory. Obviously adjust the path based on your actual Munki server setup.
# Note: This script is fairly simple, because all my manifests were in the same directory (no subdirectories). If you have a lot of subdirectories, you may want to tweak it so it does an os.walk through the subdirectories
manifests_directory='/Library/WebServer/Documents/munki_repo/manifests/'

## Define the destination manifests directory. You'll probably merge the two later, but this gives you an intermediate place to put stuff until you do.
new_manifests_directory='/Library/WebServer/Documents/munki_repo/newmanifests/'

## Define your dictionary of original manifest names and new manifest names. I just did an export to Excel from MunkiReport and then did some find/replace in a text editor. If you're clever with MySQL or have some other way to get the data in the form you want, go for whatever method works for you.
manifest_to_serial = {'ORIGINALMANIFESTNAME1': 'SERIALNUMBER1', 'ORIGINALMANIFESTNAME2': 'SERIALNUMBER2', 'ORIGINALMANIFESTNAME3': 'SERIALNUMBER3'}

# Make sure the manifests directory location exists.
if os.path.isdir(new_manifests_directory):

   # Loop through old manifests dictionary
   for old_name, serial in manifest_to_serial.items():
      # Get the full path based on the manifests path
      manifest_path=os.path.join(manifests_directory, old_name)
      # Double-check the path exists
      if os.path.isfile(manifest_path):
         # Create the destination full path
         new_manifest_path=os.path.join(new_manifests_directory, serial)
         print "New manifest path will be %s" % new_manifest_path
         # Copy the file
         shutil.copyfile(manifest_path, new_manifest_path)
         print "Copying to new manifest path"
         # Get the new display name
         # I had a weird thing where some of the old manifest names had a name and then a hyphen and then the serial number, so you can modify this to suit your organization's needs or just make the display name equal to the old name
         display_name_temp=old_name.split("-" + serial, 1)
         display_name=display_name_temp[0]
         print display_name
         # Yeah, I know there's plistlib, but I actually found it simpler to just use PlistBuddy. Again, feel free to tweak as you see fit.
         cmd='/usr/libexec/PlistBuddy -c "Add :display_name string ' + "'" + display_name + "'" + '" ' + new_manifest_path
         subprocess.call(cmd, shell=True)
      else:
         print "%s does not exist" % manifest_path
else:
   print "%s does not exist" % new_manifests_directory
