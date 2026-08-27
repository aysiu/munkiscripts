#!/bin/zsh

# Checks to see if there are sha256 mismatches between what's stored in the pkgsinfo and what's in the actual pkgs

# Change this to your actual Munki repo path
munki_repo_path='/Users/Shared/munki_repo'

pkginfo_files=$(/usr/bin/find $munki_repo_path/pkgsinfo -type f \( -iname \*.plist -o -iname \*.pkginfo \))

# Initialize errors array
errors=()

for pkginfo_file in "${(f)pkginfo_files}"; do
    /bin/echo "Checking $pkginfo_file..."
    specified_hash=$(/usr/libexec/PlistBuddy -c "Print:installer_item_hash" $pkginfo_file)
    specified_location=$(/usr/libexec/PlistBuddy -c "Print:installer_item_location" $pkginfo_file)
    # Not every pkginfo will have an installer... some are nopkgs, so let's check we got back values
    if [[ ! -z $specified_hash && ! -z $specified_location ]]; then
        actual_hash=$(/usr/bin/shasum -a 256 $munki_repo_path/pkgs/$specified_location | /usr/bin/awk -F " " '{print $1}'
)
        if [[ $actual_hash != $specified_hash ]]; then
            /bin/echo "Found mismatch."
            errors+=("$pkginfo_file has $specified_hash for $specified_location and should have $actual_hash")
        fi
    fi
done

if [[ -z ${errors[@]} ]]; then
    /bin/echo "All the hashes in the pkginfo files match the actual hashes of the installer files."
else
    /bin/echo "Found mismatch(es)..."
    for error in "${errors[@]}"; do
        /bin/echo $error
    done
fi
