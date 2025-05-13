## Munki Minimal Bootstrap Package
### Requirements
- [munkipkg](https://github.com/munki/munki-pkg)
- Ability to use [Apple Developer](https://developer.apple.com/support/certificates) signing certificate
- MDM that provides a configuration profile for Munki settings

### Usage
Modify the `build-info.plist` file, and replace `PUT IN SIGNING IDENTITY COMMON NAME` with your the signing cert you'll be using, and replace `COM.YOURORG` with your actual organization's reverse domain name.

Go to https://github.com/macadmins/munki-builds/releases/latest and download the latest Munki installer to the `payload/private/tmp` folder, and modify the `scripts/postinstall` file, and change `munki_installer=/private/tmp/munkitools-6.6.3.4704.pkg` to the actual path to the installer you downloaded and `url_test="SoftwareRepoURL: 'https://YOURORG.COM/munki_repo'"` to the actual URL that your MDM profile will set.

By default, the postinstall script will wait up to three minutes for the URL to get set, and then the script will give up. You can change `max_waiting_minutes` to a higher or lower minute value if you want.

Run `munkipkg /PATH/TO/minimal_bootstrap/package` to create your package, which you'll find in `build/minimal_bootstrap-1.0.pkg` (version number may vary, of course).

### Disclaimer
I don't use this myself. I just created it because I thought it might be helpful to others who are trying to bootstrap Munki. No warranty or support explicit or implied.
