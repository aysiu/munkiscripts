#!/bin/bash

## Put in the fqdn of your Munki server
SHORTURL='munki.yourcompany.com'

## Put in the SSID of a temporary (or permanent?) wireless network
SSID='nameofyourssid'

## Put in a password for the SSID
PASSWORD='passwordforyourssid'

# If there's an internet connection, then delete the script, because Outset doesn't do boot-once scripts with no network by default
PINGTEST=$(ping -o -t 4 $SHORTURL | grep "64 bytes")

if [ ! -z "$PINGTEST" ]; then
   sudo /bin/rm /usr/local/outset/boot-every/WirelessConnect.sh

else

   # Connect to wireless
   # Find the wireless network hardware port name
   wifiport=$(/usr/sbin/networksetup -listallhardwareports | /usr/bin/grep -A1 "Wi-Fi" | /usr/bin/sed -n -e 's/^.*Device: //p')

   # If it's not empty...
   if [ ! -z "$wifiport" ]; then 
	   # Connect to the wireless network
	   sudo /usr/sbin/networksetup -setairportnetwork $wifiport "$SSID" "$PASSWORD"
   fi

fi
