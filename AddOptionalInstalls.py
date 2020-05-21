#!/usr/local/munki/python

import os
import plistlib
import sys

# Apps to add to the SelfServeManifest
# Feel free to modify and put in whatever apps you actually want to install
# Go with the name (not the display_name) of the Munki item
default_apps = [ 'Firefox', 'GoogleChrome', 'VirtualBox' ]

# Location of the SelfServeManifest
self_serve_manifest = '/Library/Managed Installs/manifests/SelfServeManifest'

# Check that the SelfServeManifest exists
if os.path.isfile(self_serve_manifest):
    # Try to read its current contents
    try:
        manifest_file = open(self_serve_manifest, 'rb')
    except:
        print("ERROR: Unable to open {}".format(self_serve_manifest))
        sys.exit(1)
    try:
        manifest_contents = plistlib.load(manifest_file)
    except:
        print("ERROR: Unable to read contents of {}".format(self_serve_manifest))
        sys.exit(1)
    manifest_file.close()
    # Initialize test variable
    file_changed = 0
    if 'managed_installs' not in manifest_contents.keys():
        manifest_contents['managed_installs'] = []
    for default_app in default_apps:
        if default_app not in manifest_contents['managed_installs']:
            # Change test variable
            if file_changed == 0:
                file_changed = 1
            print("Adding {} to SelfServeManifest".format(default_app))
            manifest_contents['managed_installs'].append(default_app)
    # Try to write the contents back
    if file_changed == 1:
        try:
            manifest_file = open(self_serve_manifest, 'wb')
        except:
            print("ERROR: Unable to open {}".format(self_serve_manifest))
            sys.exit(1)
        try:
            plistlib.dump(manifest_contents, manifest_file)
        except:
            print("ERROR: Unable to write changes to {}".format(self_serve_manifest))
            sys.exit(1)
        manifest_file.close()
        print("Changes written back to {}".format(self_serve_manifest))
    else:
        print("Nothing changed in the SelfServeManifest file")
else:
    print("ERROR: {} does not exist".format(self_serve_manifest))
    sys.exit(1)
