#!/bin/bash

#### Purpose of Script
## Originally created to bulk-import GarageBand content .pkg files downloaded by https://github.com/cwindus/garageband, in theory you could use this for any large set of .pkg files you want to import into Munki without doing a manual munkiimport on each one

#### Other Notes
## The name, display name, and description may not be what you want. Be sure to add those in later!
## If you want all the .pkg files to require a certain item, you can append something like --requires=GarageBand to the munkiimport command in the while loop
## Likewise, you can use --update_for=GarageBand if you want them all to be updates for a particular item like GarageBand

#### User-defined variables
## Define the directory where your .pkg files are located. This directory will be looped through recursively.
pkgdir='/Users/USERNAME/Downloads/garageband/garageband'

## What is the category and developer for these .pkg files?
pkgcategory='Multimedia'
pkgdeveloper='Apple'

## Double-check that the Munki commands we want to run are available
if [ -f "/usr/local/munki/munkiimport" ] && [ -f "/usr/local/munki/makecatalogs" ]; then

   # Get the absolute path to all .pkg files in this directory and its subdirectories
   find "$pkgdir" -type f -name '*.pkg' | while read pkg; do
      # For each .pkg, import in nointeractive mode
      /usr/local/munki/munkiimport "$pkg" --nointeractive --unattended_install --category="$pkgcategory" --developer="$pkgdeveloper"
   done

   # Rebuild the catalogs
   /usr/local/munki/makecatalogs

fi
