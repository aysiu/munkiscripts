#!/usr/local/munki/python

import argparse
import copy
import csv
import os
import plistlib
import sys

######################################
#### Start user-defined variables ####

# Location of manifests folder
manifests_directory = '/Users/Shared/munki_repo/manifests/'

# Catalog order
catalog_order = [ 'development', 'testing', 'production' ]

#### End user-defined variables #####
#####################################

def list_from_string(in_string):
    # Process differently depending on whether there are multiple elements or not
    # If there is a comma, let's assume there are separate elements
    if ',' in in_string:
        try:
            out_temps = in_string.split(',')
        except:
            print("ERROR: Unable to parse {}".format(in_string))
            sys.exit(1)
    # If there is no comma, let's just make a list with a single item in it
    else:
        out_temps = [in_string]
    out_list = []
    for out_temp in out_temps:
        out_list.append(out_temp.strip())
    return out_list

def get_options():
    parser = argparse.ArgumentParser(description='Generate/modifies manifests from serial numbers in a CSV.')
    parser.add_argument('--every', help='Modify all serial manifests. Most useful for mass-removals, \
                        because there is no user / display name option.', action='store_true')
    parser.add_argument('--csv', help='Path to CSV file. Columns: 1, serial; 2, username; 3, display name. \
                        Takes precedence over the --every flag.')
    parser.add_argument('--addcatalogs', help='Catalogs to add, separated by commas.')
    parser.add_argument('--removecatalogs', help='Catalogs to remove, separated by commas.')
    parser.add_argument('--addmanifests', help='Manifests to add, separated by commas.')
    parser.add_argument('--removemanifests', help='Manifests to remove, separated by commas.')
    parser.add_argument('--addnotes', help='String to add to notes.')
    parser.add_argument('--addinstalls', help='Managed installs to add, separated by commas.')
    parser.add_argument('--removeinstalls', help='Managed installs to remove, separated by commas.')
    parser.add_argument('--adduninstalls', help='Managed uninstalls to add, separated by commas.')
    parser.add_argument('--removeuninstalls', help='Managed uninstalls to remove, separated by commas.')
    parser.add_argument('--addoptionals', help='Optional installs to add, separated by commas.')
    parser.add_argument('--removeoptionals', help='Optional installs to remove, separated by commas.')
    parser.add_argument('--addfeatured', help='Featured optional installs to add, separated by commas.')
    parser.add_argument('--removefeatured', help='Featured optional installs to remove, separated by commas.')
    args = parser.parse_args()
    if args.csv:
        csvin = args.csv
        every = False
    elif args.every:
        csvin = False
        every = args.every
    else:
        print("ERROR: You must use either the --csv or --every flag")
        sys.exit(1)
    if args.addcatalogs:
        addcatalogs = list_from_string(args.addcatalogs)
    else:
        addcatalogs = False
    if args.removecatalogs:
        removecatalogs = list_from_string(args.removecatalogs)
    else:
        removecatalogs = False
    if args.addmanifests:
        addmanifests = list_from_string(args.addmanifests)
    else:
        addmanifests = False
    if args.removemanifests:
        removemanifests = list_from_string(args.removemanifests)
    else:
        removemanifests = False
    if args.addnotes:
        addnotes = args.addnotes.strip()
    else:
        addnotes = False
    if args.addinstalls:
        addinstalls = list_from_string(args.addinstalls)
    else:
        addinstalls = False
    if args.removeinstalls:
        removeinstalls = list_from_string(args.removeinstalls)
    else:
        removeinstalls = False
    if args.adduninstalls:
        adduninstalls = list_from_string(args.adduninstalls)
    else:
        adduninstalls = False
    if args.removeuninstalls:
        removeuninstalls = list_from_string(args.removeuninstalls)
    else:
        removeuninstalls = False
    if args.addoptionals:
        addoptionals = list_from_string(args.addoptionals)
    else:
        addoptionals = False
    if args.removeoptionals:
        removeoptionals = list_from_string(args.removeoptionals)
    else:
        removeoptionals = False
    if args.addfeatured:
        addfeatured = list_from_string(args.addfeatured)
    else:
        addfeatured = False
    if args.removefeatured:
        removefeatured = list_from_string(args.removefeatured)
    else:
        removefeatured = False
    return csvin, every, addcatalogs, removecatalogs, addmanifests, removemanifests, addnotes,
                        addinstalls, removeinstalls, adduninstalls, removeuninstalls, addoptionals,
                        removeoptionals, addfeatured, removefeatured

def clean_username(dirty_username):
    if '@' in dirty_username:
        temp_username = dirty_username.lower().strip().split('@')
        cleaned_username = temp_username[0]
    else:
        cleaned_username = dirty_username.lower().strip()
    return cleaned_username

def add_to_array(add_list, array, array_key):
    if array_key not in array.keys():
        array[array_key] = []
    for add_item in add_list:
        if add_item not in array[array_key]:
            array[array_key].append(add_item)
    return array

def remove_from_array(remove_list, array, array_key):
    if array_key in array.keys():
        for remove_item in remove_list:
            if remove_item in array[array_key]:
                array[array_key].remove(remove_item)
    return array

def modify_manifest(serial, username, display_name, addcatalogs, removecatalogs, addmanifests,
                    removemanifests, addnotes, addinstalls, removeinstalls, adduninstalls,
                    removeuninstalls, addoptionals, removeoptionals, addfeatured, removefeatured):
    # Create location to save manifest to
    manifest_location = os.path.join(manifests_directory, serial)

    # Initialize test variable
    proceed_okay = 1

    # Test to see if it exists already
    if os.path.exists(manifest_location):
        # Try to get the content
        try:
            f = open(manifest_location, 'rb')
        except:
            print("ERROR: Unable to open {}".format(serial))
            proceed_okay = 0
        try:
            manifest_content = plistlib.load(f)
        except:
            print("ERROR: Unable to read {}".format(serial))
            proceed_okay = 0
        f.close()
    else:
        # Initialize dictionary of XML content
        manifest_content = {}

    # Write back changes only if it's changed, so let's keep track of what was originally there
    original_manifest_content = copy.deepcopy(manifest_content)

    # We don't want to quit out just because we weren't able to open/read one manifest, so let's proceed if we can proceed.
    if proceed_okay == 0:
        print("WARNING: Skipping {}".format(serial))
    else:
        if addcatalogs or removecatalogs:
            # Loop through the catalogs
            manifest_content['catalogs'] = []
            for catalog in catalog_order:
                # Since we emptied out the catalogs, we don't need to remove any catalogs, just make sure we aren't re-adding
                # those catalogs back
                if ((removecatalogs and catalog not in removecatalogs) or not removecatalogs) and (('catalogs' in original_manifest_content.keys() and catalog in original_manifest_content['catalogs']) or (addcatalogs and catalog in addcatalogs and catalog not in manifest_content['catalogs'])):
                    manifest_content['catalogs'].append(catalog)

        # Add display name      
        if display_name:
            manifest_content['display_name'] = display_name.strip()

        # Add user
        if username:
            manifest_content['user'] = clean_username(username)

        # Notes
        if addnotes:
            if 'notes' in manifest_content.keys():
                if addnotes in manifest_content['notes']:
                    print("Note already exists in notes")
                elif manifest_content['notes'].strip() == '':
                    manifest_content['notes'] = addnotes
                else:
                    manifest_content['notes'] += '\n' + addnotes
            else:
                manifest_content['notes'] = addnotes

        # Included manifests
        if removemanifests:
            manifest_content = remove_from_array(removemanifests, manifest_content, 'included_manifests')
        if addmanifests:
            manifest_content = add_to_array(addmanifests, manifest_content, 'included_manifests')

        # Managed installs
        if removeinstalls:
            manifest_content = remove_from_array(removeinstalls, manifest_content, 'managed_installs')
        if addinstalls:
            manifest_content = add_to_array(addinstalls, manifest_content, 'managed_installs')

        # Managed uninstalls
        if removeuninstalls:
            manifest_content = remove_from_array(removeuninstalls, manifest_content, 'managed_uninstalls')
        if adduninstalls:
            manifest_content = add_to_array(adduninstalls, manifest_content, 'managed_uninstalls')

        # Optional installs
        if removeoptionals:
            manifest_content = remove_from_array(removeoptionals, manifest_content, 'optional_installs')
        if addoptionals:
            manifest_content = add_to_array(addoptionals, manifest_content, 'optional_installs')

        # Featured installs
        if removefeatured:
            manifest_content = remove_from_array(removefeatured, manifest_content, 'featured_items')
        if addfeatured:
            manifest_content = add_to_array(addfeatured, manifest_content, 'featured_items')

        # If there were changes, Write back manifest content to the new manifest
        if original_manifest_content != manifest_content:
            if display_name:
                print("Writing changes back to {} for {}".format(serial, display_name))
            else:
                print("Writing changes back to {}".format(serial))
            try:
                f = open(manifest_location, 'wb')
            except:
                print("ERROR: Unable to open {} for writing".format(serial))
                proceed_okay = 0
            if proceed_okay == 1:
                try:
                    plistlib.dump(manifest_content, f)
                except:
                    print("ERROR: Unable to write changes back to {} for writing".format(serial))
            f.close()

def main():
    # Get options
    csvin, every, addcatalogs, removecatalogs, addmanifests, removemanifests, addnotes, addinstalls,
                        removeinstalls, adduninstalls, removeuninstalls, addoptionals, removeoptionals,
                        addfeatured, removefeatured = get_options()

    # CSV takes precedence over every
    if csvin:
        # Make sure the manifests directory exists and is writable
        if os.path.isdir(manifests_directory):
            # A CSV was supplied, use that for all data.
            if os.path.isfile(csvin):
                try:
                    infile = open(csvin, mode='r')
                except:
                    print("ERROR: Unable to open {}".format(csvin))
                    sys.exit(1)
                reader = csv.reader(infile)
                next(reader, None) # skip the header row
                for row in reader:
                    row_count = len(row)
                    serial = row[0].upper().strip()
                    if len(serial) != 12:
                        print("ERROR: Skipping {}, since it doesn't appear to be a serial number".format(serial))
                        continue
                    if row_count > 1:
                        username = row[1]
                        if row_count > 2:
                            display_name = row[2]
                        else:
                            display_name = False
                    else:
                        username = False
                        display_name = False
                    modify_manifest(serial, username, display_name, addcatalogs, removecatalogs,
                                    addmanifests, removemanifests, addnotes, addinstalls, removeinstalls,
                                    adduninstalls, removeuninstalls, addoptionals, removeoptionals, addfeatured,
                                    removefeatured)
            else:
                print("ERROR: {} doesn't exist".format(csvin))
                sys.exit(1)
        else:
            print("ERROR: {} doesn't exist".format(manifests_directory))
            sys.exit(1)
    # If no CSV is specified, but every is, let's go with all serial manifests
    elif every:
        username = False
        display_name = False
        if os.path.isdir(manifests_directory):
            for root, subdirs, files in os.walk(manifests_directory):
                for file in files:
                    # Exclude files that start with ., files that are not 12 characters long and files that
                    # are not all uppercase
                    if file.startswith('.') or len(file) != 12 or file.upper() != file:
                        continue
                    serial = file
                    modify_manifest(serial, username, display_name, addcatalogs, removecatalogs, addmanifests,
                                    removemanifests, addnotes, addinstalls, removeinstalls, adduninstalls,
                                    removeuninstalls, addoptionals, removeoptionals, addfeatured, removefeatured)
        else:
            print("ERROR: {} doesn't exist".format(manifests_directory))
            sys.exit(1)
    # No CSV and no every? Error!
    else:
        print("ERROR: You must use either the --csv or --every flag")
        sys.exit(1)

if __name__ == '__main__':
    main()
