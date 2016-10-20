#!/usr/bin/python

import os
import plistlib

######################################
#### Start user-defined variables ####

manifests_directory='/Library/WebServer/Documents/munki_repo/manifests/'

# You've got to get this somehow out of whatever reporting tool, spreadsheet, previous management system you had in place. Even if it's ARD, you can do an export of machines and serial numbers from there.
manifests_to_create = {'SERIALNUMBER1': 'DISPLAYNAME1', 'SERIALNUMBER2': 'DISPLAYNAME2', 'SERIALNUMBER3': 'DISPLAYNAME3'}

# Specify whatever catalogs and included manifests you want for this set of manifests
manifest_catalogs = ['production']
manifests_to_include =['FIRSTINCLUDED', 'SECONDINCLUDED']

#### End user-defined variables #####
#####################################

def main():

   # Make sure the manifests directory exists and is writable
   if os.path.isdir(manifests_directory) and os.access(manifests_directory, os.W_OK):
   
      # Loop through the manifests to create
      for serial,display_name in manifests_to_create.items():
         # Initialize dictionary of XML content
         manifest_content = { 'catalogs': [], 'managed_installs': [], 'managed_uninstalls': [], 'included_manifests': [] }
         # Loop through the catalogs to include
         for catalog in manifest_catalogs:
            manifest_content['catalogs'].append(catalog)
         # Add display name      
         manifest_content['display_name'] = display_name
         # Loop through the manifests to include
         for manifest in manifests_to_include:
            manifest_content['included_manifests'].append(manifest)   
         # Create location to save manifest to
         manifest_location=os.path.join(manifests_directory, serial)
         # Write back manifest content to the new manifest
         try:
            plistlib.writePlist(manifest_content, manifest_location)
         except IOError:
            print "Unable to create %s manifest with display name of %s" % (serial, display_name) 
         else:
            print "Creating %s manifest for %s" % (serial, display_name)
      # Remind the user of makecatalogs
      print "\nDon't forget to run /usr/local/munki/makecatalogs after you're done making manifests"
   else:
      print "Either %s isn't a valid directory or you don't have write permissions to that directory." % manifests_directory

if __name__ == '__main__':
   main()
