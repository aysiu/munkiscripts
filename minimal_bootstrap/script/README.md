## Munki Minimal Bootstrap Script
### Requirements
- MDM that can provide a configuration profile for Munki settings
- MDM that can run an arbitrary script as root upon Mac enrollment in the MDM

### Usage
Change `munki_installer='https://github.com/macadmins/munki-builds/releases/download/v6.6.3.4704/munkitools-6.6.3.4704.pkg'` to whatever version of Munki you want to deploy from https://github.com/macadmins/munki-builds/releases/latest

You may be using Munki to update itself, so you may not need to have this initially downloaded version always be the latest. That said, you may also not want to be 15-20 versions behind if you never update the initial version.

If you update the version, you'll also need to modify `installer_checksum='114a54c00a160eba6bff4e3590d065ad'` to be the actual md5 checksum of the downloaded .pkg (you can find it by running `md5 -q /PATH/TO/munkitools-VERSION.pkg`.

### Disclaimer
I don't use this myself. I just created it because I thought it might be helpful to others who are trying to bootstrap Munki. No warranty or support explicit or implied.
