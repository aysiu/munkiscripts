#!/bin/bash

# Uses Adobe CC as an example, but it could be any sets of items you want removed from the self-serve manifest

# Location of self-serve manifest
self_serve_manifest='/Library/Managed Installs/manifests/SelfServeManifest'

# Location of PlistBuddy executable
plistbuddy='/usr/libexec/PlistBuddy'

# Items to remove from the self-serve manifest
items_to_remove=(
	'AdobeAfterEffects2018'
	'AdobeAnimate2018'
	'AdobeAudition2018'
	'AdobeBridge2018'
	'AdobeCharacterAnimator2018'
	'AdobeDreamweaver2018'
	'AdobeFlashBuilderPremium2018'
	'AdobeFuse2018'
	'AdobeGamingSDK2018'
	'AdobeIllustrator2018'
	'AdobeInCopy2018'
	'AdobeInDesign2018'
	'AdobeLightroomClassic2018'
	'AdobeMediaEncoder2018'
	'AdobeMuse2018'
	'AdobePhotoshop2018'
	'AdobePrelude2018'
	'AdobePremierePro2018'
	'AdobeScout2018'
)

# Check to see if the self-serve manifest exists
if [[ -f "$self_serve_manifest" ]]; then

	for item in "${items_to_remove[@]}"
		do
			# See if it's in the self-serve manifest
			item_location=$("$plistbuddy" -c "Print managed_installs" "$self_serve_manifest" | /usr/bin/grep -n "$item" | /usr/bin/awk -F ":" '{print $1}')

			if [[ ! -z "$item_location" ]]; then
				# Item to delete is the number minus two
				item_to_delete=$(($item_location-2))

				"$plistbuddy" -c "Delete :managed_installs:$item_to_delete" "$self_serve_manifest"

			fi

	done
	
fi
