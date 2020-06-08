#!/usr/local/munki/python

import argparse
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
    parser.add_argument('--csv', help='Path to CSV file. Columns: 1, serial; 2, username; 3, display name', required=True)
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
    else:
        print("ERROR: Missing --csv")
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
    return csvin, addcatalogs, removecatalogs, addmanifests, removemanifests, addnotes, addinstalls, removeinstalls, adduninstalls, removeuninstalls, addoptionals, removeoptionals, addfeatured, removefeatured

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
    if add_list:
        for add_item in add_list:
            if add_item not in array[array_key]:
                array[array_key].append(add_item)
    return array

def remove_from_array(remove_list, array, array_key):
    if array_key in array.keys() and remove_list:
        for remove_item in remove_list:
            if remove_item in array[array_key]:
                array[array_key].remove(remove_item)
    return array

def modify_manifest(serial, username, display_name, addcatalogs, removecatalogs, addmanifests, removemanifests, addnotes, addinstalls, removeinstalls, adduninstalls, removeuninstalls, addoptionals, removeoptionals, addfeatured, removefeatured):
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

    # We don't want to quit out just because we weren't able to open/read one manifest, so let's proceed if we can proceed.
    if proceed_okay == 0:
        print("WARNING: Skipping {}".format(serial))
    else:
        # Loop through the catalogs
        if 'catalogs' not in manifest_content.keys():
            original_catalogs = []
        else:
            original_catalogs = manifest_content['catalogs'].copy()
        manifest_content['catalogs'] = []
        for catalog in catalog_order:
            if (catalog in original_catalogs) and ((removecatalogs and catalog not in removecatalogs) or (not removecatalogs)):
                manifest_content['catalogs'].append(catalog)
            elif addcatalogs and catalog in addcatalogs and catalog not in manifest_content['catalogs']:
                manifest_content['catalogs'].append(catalog)
            elif removecatalogs and catalog in removecatalogs and catalog in manifest_content['catalogs']:
                manifest_content['catalogs'].remove(catalog)

        # Add display name      
        if display_name:
            manifest_content['display_name'] = display_name.strip()

        # Add user
        if username:
            manifest_content['user'] = clean_username(username)

        # Notes
        if addnotes:
            if 'notes' in manifest_content.keys() and addnotes in manifest_content['notes']:
                print("Note already exists in notes")
            else:
                manifest_content['notes'] = addnotes

        # Included manifests
        manifest_content = remove_from_array(removemanifests, manifest_content, 'included_manifests')
        manifest_content = add_to_array(addmanifests, manifest_content, 'included_manifests')

        # Managed installs
        manifest_content = remove_from_array(removeinstalls, manifest_content, 'managed_installs')
        manifest_content = add_to_array(addinstalls, manifest_content, 'managed_installs')

        # Managed uninstalls
        manifest_content = remove_from_array(removeuninstalls, manifest_content, 'managed_uninstalls')
        manifest_content = add_to_array(adduninstalls, manifest_content, 'managed_uninstalls')

        # Optional installs
        manifest_content = remove_from_array(removeoptionals, manifest_content, 'optional_installs')
        manifest_content = add_to_array(addoptionals, manifest_content, 'optional_installs')

        # Featured installs
        manifest_content = remove_from_array(removefeatured, manifest_content, 'featured_items')
        manifest_content = add_to_array(addfeatured, manifest_content, 'featured_items')

        # Write back manifest content to the new manifest
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
    csvin, addcatalogs, removecatalogs, addmanifests, removemanifests, addnotes, addinstalls, removeinstalls, adduninstalls, removeuninstalls, addoptionals, removeoptionals, addfeatured, removefeatured = get_options()

    # Make sure the manifests directory exists and is writable
    if os.path.isdir(manifests_directory) and os.access(manifests_directory, os.W_OK):
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
                modify_manifest(serial, username, display_name, addcatalogs, removecatalogs, addmanifests, removemanifests, addnotes, addinstalls, removeinstalls, adduninstalls, removeuninstalls, addoptionals, removeoptionals, addfeatured, removefeatured)
        else:
            print("ERROR: {} doesn't exist".format(csvin))
            sys.exit(1)
    else:
        print("ERROR: {} doesn't exist or isn't writeable".format(manifests_directory))
        sys.exit(1)

if __name__ == '__main__':
    main()
