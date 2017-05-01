#!/usr/bin/python
import os
import plistlib
import csv
import argparse
import sys

##############################
#### Start Define CLI Arguments ####
#
def getOptionsString(optionList):
	# optionList should be a list item
	optionsString = ''
	for option in optionList:
		if option == optionList[-1]:
			optionsString += "\"%s\":\"%s\"" % (str(option.split('=')[0]), str(option.split('=')[1]))
		else:
			optionsString += "\"%s\":\"%s\"" % (str(option.split('=')[0]), str(option.split('=')[1])) + ', '
	return optionsString

parser = argparse.ArgumentParser(description='Generate manifests from serial numbers.')
parser.add_argument('--dest', help='Destination for generated manifests. Default: /Library/WebServer/Documents/munki_repo/manifests/')
parser.add_argument('--catalogs', help='Catalogs you want for this set of manifests. Example: "Production, testing"')
parser.add_argument('--manifests', help='Included manifests you want for this set of manifests. Example: "[site_default, printers"')
parser.add_argument('--serials', help='Key value pairs of serial to display name. Example: "SERIALNUMBER1:DISPLAYNAME1, SERIALNUMBER2:DISPLAYNAME2"')
parser.add_argument('--csv', help='Path to CSV file containing printer info. If CSV is provided, all other options are ignored.')
args = parser.parse_args()

#### End Define CLI Arguments #####
###################################

######################################
#### Start user-defined variables ####

# Location of manifests folder on your server
# Not overridden by supplying a csv
manifests_directory = args.dest or '/Library/WebServer/Documents/munki_repo/manifests/'

# Values can be set inline or supplied at runtime as arguments. 
# Arguments will override inline values
# Supplying a csv will take precedence over previous two methods

# Serial numbers and display names for manifests to be created
# Should be supplied in the form {"SERIALNUMBER1":"DISPLAYNAME1", "SERIALNUMBER2":DISPLAYNAME2"}
manifests_to_create = {}

# Specify whatever catalogs and included manifests you want for this set of manifests
manifest_catalogs = []
manifests_to_include = []

#### End user-defined variables #####
#####################################


def write_manifest(serial, display_name, catalogs, manifests):
	# Initialize dictionary of XML content
	manifest_content = { 'catalogs': [], 'managed_installs': [], 'managed_uninstalls': [], 'included_manifests': [] }

	# Loop through the catalogs to include
	for catalog in catalogs:
		manifest_content['catalogs'].append(catalog)

	# Add display name      
	manifest_content['display_name'] = display_name

	# Loop through the manifests to include
	for manifest in manifests:
		manifest_content['included_manifests'].append(manifest)

	# Create location to save manifest to
	manifest_location = os.path.join(manifests_directory, serial)

	# Write back manifest content to the new manifest
	try:
		plistlib.writePlist(manifest_content, manifest_location)
	except IOError:
		print "Unable to create %s manifest with display name of %s" % (serial, display_name) 
	else:
		print "Creating %s manifest for %s" % (serial, display_name)


#### Run Program #####
######################

# Make sure the manifests directory exists and is writable
if os.path.isdir(manifests_directory) and os.access(manifests_directory, os.W_OK):
	if args.csv:
		# A CSV was supplied, use that for all data.
		with open(args.csv, mode='r') as infile:
			reader = csv.reader(infile)
			next(reader, None) # skip the header row

			for row in reader:
				serial = row[0]
				display_name = row[1]
				catalogs = [x.strip() for x in row[2].split(',')]
				manifests = [x.strip() for x in row[3].split(',')]

				# Each row contains 4 elements: Serial, Display Name, Catalogs, Manifests
				write_manifest(serial, display_name, catalogs, manifests)
				
	else:
		# Parse list of serials from cli args
		if args.serials:
			serials_array = args.serials.split(',')
			for pair in serials_array:
				pairs_array = pair.split(':')
				manifests_to_create[pairs_array[0].strip()] = pairs_array[1].strip()
		else:
			# Exit on an empty array of serials with an error message
			print >> sys.stderr, ("ERROR: No serials supplied, exiting")
			sys.exit(1)

		if args.catalogs:
			manifest_catalogs = [x.strip() for x in args.catalogs.split(',')]

		if args.manifests:
			manifests_to_include = [x.strip() for x in args.manifests.split(',')]

		# Loop through the manifests to create
		for serial,display_name in manifests_to_create.items():
			write_manifest(serial, display_name, manifest_catalogs, manifests_to_include)

	# Remind the user of makecatalogs
	print "\nDon't forget to run /usr/local/munki/makecatalogs after you're done making manifests"

else:
	print >> sys.stderr, ("ERROR: Manifest directory doesn't exist or isn't writeable")
	sys.exit(1)





