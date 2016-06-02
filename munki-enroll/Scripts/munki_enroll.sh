#!/bin/sh 

##### Much more complicated implementation of the original Munki-Enroll
##### This has different logic based on whether the original manifest (to be included) is set up for "individual" or not.
##### If it's "individual," the script grabs the user's full name and the computer's serial number.
##### If it's not "individual," the script just grabs the computer's name (Munki-Enroll's original behavior)
##### This version of the script also assumes you have an https-enabled Munki server with basic authentication
##### Change NAMEOFORIGINALMANIFESTTHATINDICATESINDIVIDUAL and https://yourmunkiserver.com/path/to/munki-enroll/enroll.php
##### Also change YOURLOCALADMINACCOUNT

## User-set variables
# Individual ClientIdentifier
INDIVIDUAL="NAMEOFORIGINALMANIFESTTHATINDICATESINDIVIDUAL"
# Change this URL to the location fo your Munki Enroll install
SUBMITURL="https://yourmunkiserver.com/path/to/munki-enroll/enroll.php"

# Get the length of the individual string
INDLENGTH=${#INDIVIDUAL}

# Gather computer information
IDENTIFIER=$( defaults read /Library/Preferences/ManagedInstalls ClientIdentifier )

# If it's the individual (or the first part of the name matches that)...
if [ "${IDENTIFIER:0:$INDLENGTH}" == "$INDIVIDUAL" ]; then

   # Initialize hostname string
   HOSTNAME=''

   # Make the "hostname" into the primary user and then the serial number
   
   # Get the primary user
   PRIMARYUSER=''
   # This is a little imprecise, because it's basically going by process of elimination, but that will pretty much work for the setup we have
   cd /Users
   for u in *; do
      if [ "$u" != "Guest" ] && [ "$u" != "Shared" ] && [ "$u" != "YOURLOCALADMINACCOUNT" ]; then
         PRIMARYUSER="$u"
      fi
   done
   
   if [ "$PRIMARYUSER" != "" ]; then
   
      HOSTNAME+=$(dscl . -read /Users/"$u" dsAttrTypeStandard:RealName | sed 's/RealName://g' | tr '\n' ' ' | sed 's/^ *//;s/ *$//' | sed 's/ /-/g')   
      HOSTNAME+="-"
   
   fi
   
   # There should always be a primary user... if not, then just make it the serial number
   
      # Get the serial number
      HOSTNAME+=$(system_profiler SPHardwareDataType | awk '/Serial Number/ { print $4; }')
   
else
   
   # Otherwise, make the "hostname" into the actual computer name
   HOSTNAME=$( scutil --get ComputerName | sed 's/ /-/g')

fi

# Get the authorization information
AUTH=$( defaults read /var/root/Library/Preferences/ManagedInstalls.plist AdditionalHttpHeaders | awk -F 'Basic ' '{print $2}' | sed 's/.$//' | base64 --decode )

# Application paths
CURL="/usr/bin/curl"

$CURL --max-time 5 --silent --get \
    --data-urlencode "hostname=${HOSTNAME}" \
    --data-urlencode "identifier=${IDENTIFIER}" \
    -u "$AUTH" "$SUBMITURL"

  defaults write /Library/Preferences/ManagedInstalls ClientIdentifier "$HOSTNAME"
 
exit 0
