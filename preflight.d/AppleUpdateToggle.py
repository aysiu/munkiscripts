#!/usr/bin/python
# encoding: utf-8
''' Preflight script'''

import os
import sys

# This may not be necessary if this is the preflight script and not a preflight script in a directory (e.g., created by MunkiReport)
sys.path.insert(0,'/usr/local/munki') # From MunkiReport preflight code TODO: make this relative

from munkilib import munkicommon
from munkilib import FoundationPlist

def main():
    '''Main'''
    # get runtype (based on MunkiReport preflight code)
    if (len(sys.argv) > 1):
        runtype = sys.argv[1]
    else:
        runtype = 'custom'

    # Get the current Apple updates preference
    munki_prefs_location='/Library/Preferences/ManagedInstalls.plist'

    # Make sure the preferences location exists (it should)
    if os.path.exists(munki_prefs_location):

        # Get the current preferences into a list
        munki_prefs=FoundationPlist.readPlist(munki_prefs_location)
    
        # Check the Apple updates preference exists
        if 'InstallAppleSoftwareUpdates' in munki_prefs:

            # Assign the current preference to a temporary variable
            InstallAppleSoftwareUpdates=munki_prefs['InstallAppleSoftwareUpdates']

        else:
        
            # If the Apple updates preference doesn't exist...

            # Let's assign it to the temporary variable
            InstallAppleSoftwareUpdates = False
            
            # And also add it to the list
            munki_prefs['InstallAppleSoftwareUpdates'] = False

        # If the runtype is manualcheck, turn off Apple updates
        if runtype == 'manualcheck' and InstallAppleSoftwareUpdates == True:

            InstallAppleSoftwareUpdates=False

        # Any other scenario, turn on Apple updates
        else:
            InstallAppleSoftwareUpdates = True
        
        # If the preference has changed, write it back to the preferences file
        if InstallAppleSoftwareUpdates != munki_prefs['InstallAppleSoftwareUpdates']:
            munki_prefs['InstallAppleSoftwareUpdates']=InstallAppleSoftwareUpdates
            FoundationPlist.writePlist(munki_prefs, munki_prefs_location)

if __name__ == '__main__':
    main()
