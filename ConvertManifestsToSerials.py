#!/usr/bin/python

#### This script will copy/convert named manifests to serial number manifests
#### This isn't meant out of the box to work on any Munki repository. This is just something I (aysiu) created that I found useful in its current form for my organization, but that I also thought others could adapt for their own needs... so read it over carefully, and make adjustments as fits your own organization's needs. For example, this doesn't walk through subdirectories. It just assumes all your manifests to be converted are in the top-level directory.
#### Also keep in mind this does nothing to included manifests that shouldn't have a serial number, so you'll probably want to migrate those over later without modification.

import os
import plistlib

## Define the source manifests directory. Obviously adjust the path based on your actual Munki server setup.
manifests_directory='/Library/WebServer/Documents/munki_repo/manifests/'

## Define the destination manifests directory. You'll probably merge the two later, but this gives you an intermediate place to put stuff until you do.
new_manifests_directory='/Library/WebServer/Documents/munki_repo/newmanifests/'

## Define your dictionary of original manifest names and new manifest names. I just did an export to Excel from MunkiReport and then did some find/replace in a text editor. If you're clever with MySQL or have some other way to get the data in the form you want, go for whatever method works for you.
manifest_to_serial = {'ORIGINALMANIFESTNAME1': 'SERIALNUMBER1', 'ORIGINALMANIFESTNAME2': 'SERIALNUMBER2', 'ORIGINALMANIFESTNAME3': 'SERIALNUMBER3'}

def main():
   # Make sure the manifests directory location exists and is writable to
   if os.path.isdir(new_manifests_directory) and os.access(new_manifests_directory, os.W_OK):

      # Loop through old manifests dictionary
      for old_name, serial in manifest_to_serial.items():
         # Get the full path based on the manifests path
         manifest_path=os.path.join(manifests_directory, old_name)
         print "Old manifest path was %s" % manifest_path
         # Double-check the path exists
         if os.path.isfile(manifest_path):
            # Create the destination full path
            new_manifest_path=os.path.join(new_manifests_directory, serial)
            # Get the new display name
            # I had a weird thing where some of the old manifest names had a name and then a hyphen and then the serial number, so you can modify this to suit your organization's needs or just make the display name equal to the old name
            display_name_temp=old_name.split("-" + serial, 1)
            display_name=display_name_temp[0]
            print "The display name will be %s" % display_name
            # Get old manifest information into a dictionary
            manifest_content=plistlib.readPlist(manifest_path)
            # Change the display name to be display_name in the dictionary
            manifest_content['display_name'] = display_name
            # Write back the modified dictionary contents to the new manifest location
            plistlib.writePlist(manifest_content, new_manifest_path)
            print "Creating new manifest at %s" % new_manifest_path
         else:
            print "%s does not exist" % manifest_path
   else:
      print "%s does not exist" % new_manifests_directory
if __name__ == '__main__':
   main()
