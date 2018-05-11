#!/usr/bin/python

'''
This script moves all top-level Munki manifests to the top-level of the manifests directory and then moves all included manifests into a subfolder of the manifests folder.

At the end of the script, your original manifests folder remains untouched. If you like the results, you can replace your old manifests folder with the new one this script generates.
'''

import os
import plistlib
import shutil
import sys
import time

###########################################################################
########## Modify these variables to fit your situation ###################

# Top-level manifest directory
manifests='/Volumes/munki_repo/manifests'

# Name of subfolder to put included manifests in. Cannot be blank or null for obvious reasons (no point in running this script if you aren't putting included manifests in a subfolder), but also because it will break the copy_modify_manifests function.
subfolder_name='groups'

###########################################################################
###########################################################################

# Copy to the new manifest structure location and then modify the manifest
def copy_modify_manifests(old_manifest, old_root, new_manifest_folder, subfolder, is_included):
	print "Processing %s" % old_manifest
	# Copy the manifest to the new manifest structure location
	if is_included==False:
		new_path=os.path.join(new_manifest_folder, old_manifest)
	else:
		new_path=os.path.join(new_manifest_folder, subfolder, old_manifest)
	old_path=os.path.join(old_root, old_manifest)
	try:
		shutil.copyfile(old_path, new_path)
	except:
		print "Copy of %s failed" % old_manifest
		sys.exit(1)

	# Get the plist information from this manifest
	plist=plistlib.readPlist(new_path)

	# Modify the paths to the included manifests
	if 'included_manifests' in plist:
		old_includes=plist['included_manifests']
		# Even if the key itself exists, it may be an empty array, so check to see if it's empty or not
		if old_includes:
			# Create a new list to store the modified values
			new_includes=[]
			# Loop through the includes, modify them, and put them in the new includes
			for old_include in old_includes:
				new_include=os.path.join(subfolder, old_include)
				new_includes.append(new_include)
			plist['included_manifests']=new_includes

	# Write back the modified plist information
	try:
		plistlib.writePlist(plist, new_path)
	except:
		print "Could not write back plist changes to %s" % old_manifest
		sys.exit(1)

# Main
def main():

	# Make sure the manifest directory exists
	if os.path.isdir(manifests):

		# Create new directory to put any modified manifests
		modified_manifests=manifests + '_' + str(int(time.time()))

		# New subdirectory path, too
		new_subfolder=os.path.join(modified_manifests, subfolder_name)

		# The chances that a new directory with the exact timestamp of now already exists is low, but we should double-check that directory doesn't already exist
		if not os.path.isdir(modified_manifests) and not os.path.isdir(new_subfolder):
			# print "The directory with the new manifest structure will be %s" % modified_manifests
			# Create the new manifest directory and subfolder
			try:
				os.makedirs(new_subfolder)
			except:
				print "Unable to make directory for new manifest structure" % modified_manifests
				sys.exit(1)

			# Create a dictionary that stores any manifests that are not included in any other manifests
			top_levels={}
			
			# Create a list that stores any included manifests
			included_manifests={}

			# Loop through the manifests
			for root, dirs, files in os.walk(manifests):
				for file in files:
					# Skip files that start with a period
					if file.startswith("."):
						continue
					# Get the full path to the file
					fullfile = os.path.join(root, file)
					# If it's not in the included manifests list or the top level list, add it to the top level list
					if file not in top_levels and file not in included_manifests:
						top_levels[file]=root
					# Get the included manifests for this manifest
					current_manifest=plistlib.readPlist(fullfile)
					# Check if the key itself exists
					if 'included_manifests' in current_manifest:
						current_includes=current_manifest['included_manifests']
						# Even if the key itself exists, it may be an empty array, so check to see if it's empty or not
						if current_includes:
							# Loop through each of the included manifests
							for current_include in current_includes:
								# If it's in the top_levels manifest list, take it out
								if current_include in top_levels:
									del top_levels[current_include]
								# If it's not in the included list, add it
								if current_include not in included_manifests:
									included_manifests[current_include]=root
			# Now that we know which manifests are top-level manifests and which are included ones, let's loop through both sets
			# Loop through the top-level manifests
			for top_level in top_levels:
				copy_modify_manifests(top_level, top_levels[top_level], modified_manifests, subfolder_name, False)
			# Loop through the included manifests, which themselves may include other manifests
			for included_manifest in included_manifests:
				copy_modify_manifests(included_manifest, included_manifests[included_manifest], modified_manifests, subfolder_name, True)

		else:
			print "%s already exists as a directory." % modified_manifests
			sys.exit(1)
	else:
		print "%s is not a valid manifests folder." % manifests
		sys.exit(1)

if __name__ == '__main__':
	main()
