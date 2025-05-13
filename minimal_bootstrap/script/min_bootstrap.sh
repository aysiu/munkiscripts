#!/bin/zsh

# Maximum minutes to wait until SoftwareRepoURL set
max_waiting_minutes=5

# Convert minutes to seconds
max_waiting_seconds=$((max_waiting_minutes * 60))

# URL of Munki installer to download
munki_installer='https://github.com/macadmins/munki-builds/releases/download/v6.6.5.4711/munkitools-6.6.5.4711.pkg'

# Where to download the installer to
installer_location=/private/tmp/munkitools.pkg

# md5 checksum for downloaded installer
installer_checksum='4ce74641ba15b2b067d1863886c34f14'

# Line you expect to get back from SoftwareRepoURL setting
url_test="SoftwareRepoURL: 'http://localhost/munki_repo'"

# Location of the managedsoftwareupdate command
managedsoftwareupdate=/usr/local/munki/managedsoftwareupdate

/bin/echo "Fetching Munki installer..."
/usr/bin/curl -L $munki_installer -o $installer_location

if [[ ! -f $installer_location ]]; then
    /bin/echo "$ERROR: $installer_location missing!"
    exit 1
fi

actual_checksum=$(/sbin/md5 -q $installer_location)

if [[ $actual_checksum != $installer_checksum ]]; then
    /bin/echo "ERROR: Checksum of $installer_location is $actual_checksum instead of $installer_checksum"
    exit 1
fi

/bin/echo "Installing $munki_installer..."
/usr/sbin/installer -pkg $installer_location -target /

if [[ ! -f $managedsoftwareupdate ]]; then
    /bin/echo "ERROR: Even though Munki installed, $managedsoftwareupdate is missing!"
    exit 1
fi

# Initialize counter in seconds waited
counter=0

# Presumably, the MDM would send down a configuration profile to set the Munki settings
/bin/echo "Waiting for Munki settings..."
while ! /usr/local/munki/managedsoftwareupdate --show-config | /usr/bin/grep "$url_test"; do
    if [[ $counter -gt $max_waiting_seconds ]]; then
    	/bin/echo "ERROR: Waited more than $max_waiting_seconds for $url_test. Giving up..."
    	exit 1
    fi
    /bin/echo "$url_test not present yet. Waited $counter seconds so far..."
    /bin/sleep 2
    counter=$((counter + 2))
done

/bin/echo "$url_test now present!"

/bin/echo "Setting Munki bootstrap mode..."
/usr/local/munki/managedsoftwareupdate --set-bootstrap-mode

/bin/echo "Logging out..."
/usr/bin/osascript -e 'tell app "loginwindow" to  «event aevtrlgo»'
