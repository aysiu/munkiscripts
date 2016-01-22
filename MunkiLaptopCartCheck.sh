#!/bin/sh

# Modification of code from https://github.com/jmartinez0837/Munki-Overnight/blob/master/overnightMunki.sh
# Took out all the stuff about checking the system time and shutting down, because that's happening outside the script via NoSleep and the LaunchDaemon
# NOTE: This Requires NoSleep https://github.com/integralpro/nosleep be installed with the "Command-Line Interface"

#check system battery 
battPercentage=$(pmset -g batt | grep "InternalBattery-0" | cut -c 21-23 | sed s/\%//)

echo "$(date) - Checking to see if the battery level is enough to run updates." >> /Library/Logs/MunkiLaptopCart.log

# Make sure the battery percentage is greater than 50
if [ "$battPercentage" -gt 50 ] ; then

	echo "$(date) - Battery level enough at $battPercentage. Checking to ping the Munki server." >> /Library/Logs/MunkiLaptopCart.log
		
	#wait until we can talk to munki server before continuing
	until /sbin/ping -c 1 -t 90 munki.siprep.org; do /sbin/sleep 3; done
		
	#use --auto in case laptop does go to sleep, when opened there will be no visual to the user and they can still log in
	/usr/local/munki/managedsoftwareupdate --auto
			
	# Write to the log
	echo "$(date) - Munki run." >> /Library/Logs/MunkiLaptopCart.log
			
else
	# Write to the log
	echo "$(date) - Battery too low at $battPercentage to run Munki updates." >> /Library/Logs/MunkiLaptopCart.log

fi	

exit 0
