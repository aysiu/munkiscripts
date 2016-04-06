#!/usr/bin/python

### More details here on how to implement: https://github.com/munki/munki/wiki/Conditional-Items#admin-provided-conditions
## This should go in /usr/local/munki/conditions and be marked executable
## On the manifest, the condition would look like ping_time < 3.000

from Foundation import CFPreferencesCopyAppValue
import os
import plistlib
import subprocess

## Put in the address of your Munki server
MunkiServer="your.munki.server.com"

# Read the location of the ManagedInstallDir from ManagedInstall.plist
BUNDLE_ID = 'ManagedInstalls'
pref_name = 'ManagedInstallDir'
managedinstalldir = CFPreferencesCopyAppValue(pref_name, BUNDLE_ID)

# Make sure we're outputting our information to "ConditionalItems.plist"
conditionalitemspath = os.path.join(managedinstalldir, 'ConditionalItems.plist')

def getPingTime():

   ## By default, define a ping time, in case we don't define one later... since a lower ping time is faster, we'll default to it be unusually high
   PingTime=100000.000

   ## Test the connection speed
   cmd='ping -c 5 ' + MunkiServer + ' | awk -F "time=" \'{ print $2 }\' | sed s/\'ms\'/\'\'/g'
   PingTest=subprocess.check_output(cmd, shell=True)

   # Get the ping results into a list based on the carriage returns
   Pings=PingTest.split("\n")

   # Filter out the empty values in the list
   Pings=filter(None, Pings)

   # Test that there are any values (there should be)
   if Pings:

      # Convert into decimals all the strings in the list
      Pings=[float(i) for i in Pings]

      # Find the connection speed based on the average ping duration
      PingTime=sum(Pings)/len(Pings)

   # Define dictionary to feed back to conditional items
   ping_dict = dict(
      ping_time = PingTime
      )

   # CRITICAL!
   if os.path.exists(conditionalitemspath):
      # "ConditionalItems.plist" exists, so read it FIRST (existing_dict)
      existing_dict = plistlib.readPlist(conditionalitemspath)
      # Create output_dict which joins new data generated in this script with existing data
      output_dict = dict(existing_dict.items() + ping_dict.items())
   else:
      # "ConditionalItems.plist" does not exist,
      # output only consists of data generated in this script
      output_dict = ping_dict

   # Write out data to "ConditionalItems.plist"
   plistlib.writePlist(output_dict, conditionalitemspath)

getPingTime()
