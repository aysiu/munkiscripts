#!/usr/bin/python

import os
import plistlib

# Change this to match your actual Munki repo path
manifest_path='/Library/WebServer/Documents/munki_repo/manifests'

# Change this to the name of the item you want to remove (case and spaces matter)
item_to_remove='Name of Offending Item'

removal_type='managed_installs'

# Loop through the manifests directory
for root, dirs, files in os.walk(manifest_path):
    for file in files:

        # Get the full path to the file
        file_path=os.path.join(root,file)

        # Omit files that start with a period
        if os.path.exists(file_path) and file[0]!=".":

            # Even then, it's possible some files in the directory (and subdirectories) may not be actual manifests, so let's just TRY to read the plist
            try:

                # Read the contents of the manifest
                file_contents=plistlib.readPlist(file_path)
            except:

                # If the contents can't be read with plistlib, say so
                print "%s is not a valid .plist" % file

            # If the offending item is in the removal type...
            if removal_type in file_contents and item_to_remove in file_contents[removal_type]:
                print 'Removing %s from %s' % (file_contents[removal_type], file)

                # Remove the offending item
                file_contents[removal_type].remove(item_to_remove)

                # Write the changes back to the manifest
                plistlib.writePlist(file_contents,file_path)
