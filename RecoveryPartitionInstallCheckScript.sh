#!/bin/bash

# Fill in the version number to check for
versionToCheck="10.11.6"

# First, check to see if there is a recovery partition

partitionCheck=$(diskutil list | grep "Recovery HD")

# See if it's empty
if [ -z "$partitionCheck" ]; then

	# Since it's empty, the recovery partition is not installed
	exit 0

# If it's not empty, it may be installed... let's check the receipt version
else
	# Get the version of the recovery partition installed
	recoveryVersion=$(pkgutil --pkg-info se.gu.it.RecoveryPartitionInstaller.pkg | grep "version" | awk -F ": " '{print $2}')
	
	# Check the version
	if [ "$recoveryVersion" == "$versionToCheck" ]; then
		# It's the matching version, so installed
		exit 1

	else
		# Version doesn't match or there is no .pkg receipt, it's not installed
		exit 0

	# End checking for .pkg version
	fi

# End checking for existence of recovery partition
fi
