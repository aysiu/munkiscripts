#!/bin/bash

# .plist location
plist='/var/root/fderekey.plist'

# Double-check that the .plist exists
if [[ -f "$plist" ]]; then

	# Since it exists, let's get the current recovery key
	recovery=$(/usr/bin/defaults read "$plist" RecoveryKey)

	# Let's test it to make sure it's valid
	output=$(/usr/bin/expect -c "
		spawn /usr/bin/fdesetup validaterecovery
		expect \"Enter the current recovery key:\"
		send \"$recovery\n\"
		expect eof")

	# See if the output contains the word "true"
	output_test=$(echo "$output" | grep "true")

	if [[ -z "$output_test" ]]; then

		# If "true" wasn't in there, it's not installed
		#"echo it's not installed"
		exit 0

	else
		# If "true" was in there, it's installed
		#echo "It's installed"
		exit 1

	fi

else

	# If the .plist doesn't exist, it's not installed
	#echo "$plist does not exist, so it's not installed"
	exit 0

fi
