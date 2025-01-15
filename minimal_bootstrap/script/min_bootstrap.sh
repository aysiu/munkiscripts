#!/bin/zsh

munki_installer='https://github.com/macadmins/munki-builds/releases/download/v6.6.3.4704/munkitools-6.6.3.4704.pkg'
installer_location=/private/tmp/munkitools.pkg
installer_checksum='114a54c00a160eba6bff4e3590d065ad'
url_test="SoftwareRepoURL: 'http://localhost/munki_repo'"
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

# Presumably, the MDM would send down a configuration profile to set the Munki settings
/bin/echo "Waiting for Munki settings..."
while ! /usr/local/munki/managedsoftwareupdate --show-config | /usr/bin/grep "$url_test"; do
    /bin/echo "$url_test not present yet. Waiting..."
    /bin/sleep 2
done

/bin/echo "$url_test now present!"

/bin/echo "Setting Munki bootstrap mode..."
/usr/local/munki/managedsoftwareupdate --set-bootstrap-mode

/bin/echo "Logging out..."
/usr/bin/osascript -e 'tell app "loginwindow" to  «event aevtrlgo»'
