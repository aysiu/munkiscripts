#!/bin/bash

####### To be used as a preinstall script for http://magervalp.github.io/CreateUserPkg/
####### Checks for wrong user ID on existing account

###### Define desired User ID
desiredID="499"

###### Define short username
shortUsername="administrator"

# See if the account already exists
accountSearch=$(/usr/bin/dscl . -list /Users | /usr/bin/grep "^$shortUsername$")

if [ "$accountSearch" == "$shortUsername" ]; then
   #printf "$shortUsername exists.\n"
   # See if it has the wrong user id
   oldUserID=$(/usr/bin/dscl . -read /Users/"$shortUsername" UniqueID | /usr/bin/awk -F ": " '{print $2}')

   if [ "$oldUserID" != "$desiredID" ]; then
      #printf "$shortUsername has $oldUserID instead of $desiredID.\n"
      # Make sure the user isn't logged in
      loggedInUser=$(ls -l /dev/console | /usr/bin/awk '/ / { print $3 }')

      if [ "$loggedInUser" == "$shortUsername" ]; then
         printf "$shortUsername is logged in. Cannot proceed.\n"
         exit 1
         
      else
         # Make sure the desired ID is available
         currentOwner=$(/usr/bin/dscl . -list /Users UniqueID | /usr/bin/grep "$desiredID")

         if [ -z "$currentOwner" ]; then
            #printf "$desiredID is available. Changing $shortUsername ID to $desiredID.\n"
            # Change the user ID
            /usr/bin/dscl . -change /Users/"$shortUsername" UniqueID "$oldUserID" "$desiredID"

            # See if the directory exists (the user may have been created but never logged in
            if [ -d "/Users/$shortUsername" ]; then
               # /usr/bin/printf "/Users/$shortUsername exists, so changing ownership to $desiredID.\n"
               # Change ownership to the new ID
               /usr/sbin/chown -R "$desiredID" /Users/"$shortUsername"
            fi

         else
            # If the user ID isn't available, then abort
            /usr/bin/printf "User ID $desiredID is already taken by another user.\n"
            exit 1      
           
         # End checking to see if the desired ID is available
         fi
      # End checking to see if the user is logged in
      fi
   # End checking to see if user has wrong ID
   fi
# End checking to see if the user exists
fi
