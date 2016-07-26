#!/bin/bash

# Create a variable to see if a recovery partition exists

testVariable=$(diskutil list | grep "Apple_Boot")

# If it's empty, it's not installed
if [ -z "$testVariable" ]; then

	exit 0

# If it's not empty, it's installed

else

	exit 1
	
fi
