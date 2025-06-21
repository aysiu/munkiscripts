# update_selfservemanifest_item
This is a pseudo-payload-free package that will allow you to update the name of an item in the Munki SelfServeManifest file.

In order to have the package leave a receipt, there has to be a payload, so leave empty the "placeholder" file as the payload.

Update the postinstall script's variables at the top to reflect the old item name you want to update to the new item name.

Use [https://github.com/munki/munki-pkg](munkipkg) to create the package.

Example: `munkipkg ~/Downloads/munkiscripts/update_selfservemanifest_item`

You can then import the newly built "package" into your Munki repo to distribute to your client Macs.