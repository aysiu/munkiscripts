## Example custom package to add one icon to the dock
### Prerequisites
- [munkipkg](https://github.com/munki/munki-pkg) - Of course, you can use something like [Packages](http://s.sudre.free.fr/Software/Packages/about.html) instead to create a custom package, but the example used here is munkipkg specifically.
- [Outset](https://github.com/macadmins/outset/) - this example, as given, leverages Outset's login-once subfolder.
- [docklib](https://github.com/homebysix/docklib) - Some people prefer [dockutil](https://github.com/kcrawford/dockutil). You'd have to adjust a few things in the Outset script to use `dockutil` instead. Depending on what you're trying to do, `dockutil` may even be easier, as you can use the `--allhomes` flag, so you may not even need an Outset script. If you do stick with `docklib`, it's automatically included in [the MacAdmins Python](https://github.com/macadmins/python), which this example munkipkg package uses.

### Introduction
This isn't so much provisioning an initial dock for a freshly "imaged" Mac but more a case of "I just want to add one Dock icon that can be easily removed as well." It's using GIMP as an example, but you can easily adjust it to be whatever app you want to add a Dock shortcut for.

The logic is basically "Deliver this Outset script that runs at next login, but if someone is already logged in now, run the script as that user, and then delete the Outset script, so it doesn't run again at next login."

### Usage
- Modify the gimp_dock/payload/usr/local/outset/login-once/gimp_dock.py file to add the app you actually want to add. Optional but recommended: change the filename from `gimp_dock.py` if you're not adding GIMP.
- Modify the gimp_dock/scripts/postinstall file to point to the correct dock script name.
- Optional but recommended: modify the gimp_dock/build-info.plist file to name the package something related to the app you're trying to add to the Dock.
- Optional but recommended: modify gimp_dock itself to reference the app you're trying to add to the Dock.

Run a command similar to `munkipkg ~/Desktop/gimp_dock` but using the actual munkipkg project name and the actual path to it. That will build the package.

Deliver the package however you usually deliver packages (via [Munki](https://github.com/munki/munki) or MDM or some other mechanism). If you're using Munki, you can make the package an `update_for` the actual app's item in the Munki repo.
