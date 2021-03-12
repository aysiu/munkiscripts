#!/usr/local/munki/munki-python

import os
from signal import SIGKILL
from subprocess import PIPE, Popen
from sys import exit

# Define thresholds at the top of the script, so they can be easily tweaked
## How many times a particular PID repeats, after which it should be killed
offending_threshold = 3
## How many lines to read from the end of the ManagedSoftwareUpdate.log
lines_threshold = 60

# Offending line to look for multiple instances of
offending_line = 'Another instance of managedsoftwareupdate is running as pid '

# managedsoftwareupdate location
managedsoftwareupdate = '/usr/local/munki/managedsoftwareupdate'

def get_log_location():
    '''
    Gets location of Munki log, in case it's not in the default location
    '''
    # Double-check managedsoftwareupdate exists
    if not os.path.isfile(managedsoftwareupdate):
        print("ERROR: {} does not exist, so we can't determine log file location. "
            "Exiting...".format(managedsoftwareupdate))
        exit(1)
    # Find the location of the log file, just in case it's not in the default location
    cmd = [ managedsoftwareupdate, '--show-config' ]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf8')
    out, err = p.communicate()
    if err:
        print('ERROR: Unable to run {} successfully to get log location. '
            'Exiting...'.format(cmd))
        exit(1)
    else:
        # Initialize munki_log variable
        munki_log = False
        # Try to get the log location
        output_lines = out.splitlines()
        for output_line in output_lines:
            if 'LogFile:' in output_line:
                log_file_info = output_line.split("'")
                if len(log_file_info) > 0:
                    munki_log = log_file_info[1]
        if not munki_log:
            print('ERROR: Unable to determine location of Munki log. Exiting...')
            exit(1)
    return munki_log

def get_log_contents(munki_log):
    '''
    Gets the actual lines in the Munki log file
    '''
    # Try to open the file
    try:
        f = open(munki_log, 'r')
    except:
        print("ERROR: Can't open {}. Exiting...".format(munki_log))
        exit(1)
    # If we can open the Munki log, let's read it
    try:
        log_lines = f.readlines()
    except:
        print('ERROR: Unable to get contents of {}. Exiting...'.format(munki_log))
    return log_lines

def get_repeating_instance(log_lines):
    '''
    Finds out which repeating Munki instace there is (if any)
    '''
    # Dictionary for "Another instance of managedsoftwareupdate is running" warnings
    repeating_instance = {}
    # Also start counter for how many lines have been read
    counter = 0

    # Loop backwards through the log file
    for log_line in reversed(log_lines):
        # Don't read more than the threshold number of lines
        if counter > lines_threshold:
            break
        # Check to see if the offending line is in the log
        if offending_line in log_line:
            # Get the PID from the log string
            offending_pid = log_line.split(offending_line)[1].replace('.', '').strip()
            # If this is the first time any offending PID exists, populate the dictionary
            if 'pid' not in repeating_instance.keys():
                repeating_instance['pid'] = offending_pid
                repeating_instance['count'] = 1
            # Otherwise, if the offending PID is the same as the previous one, up the counter
            elif repeating_instance['pid'] == offending_pid:
                repeating_instance['count'] += 1
            # If the offending PID has switched, the repeating has probably stopped
            else:
                break
        # Increment the counter
        counter += 1
    if 'count' in repeating_instance.keys() and repeating_instance['count'] > offending_threshold:
        return repeating_instance
    else:
        return False

def kill_repeating_instance(repeating_instance):
    '''
    Kills the repeating instance PID
    '''
    print('Going to kill {}, which occurred {} times recently.'.format(repeating_instance['pid'], repeating_instance['count']))
    try:
        os.kill(int(repeating_instance['pid']), SIGKILL)
    except:
        print('ERROR: Unable to kill PID {}'.format(repeating_instance['pid']))
        exit(1)

def main():
    '''
    Main function
    '''
    # Get the Munki log location
    munki_log = get_log_location()

    # Double-check the log exists
    if not os.path.isfile(munki_log):
        print("ERROR: Munki log is supposed to be {} but doesn't exist. "
            "Exiting...".format(munki_log))
        exit(1)
    # Get the contents of the log
    log_lines = get_log_contents(munki_log)

    # Analyze the log lines to get a repeating instance (if there is one)
    repeating_instance = get_repeating_instance(log_lines)

    # Kill repeating instance
    if repeating_instance:
        kill_repeating_instance(repeating_instance)

if __name__ == '__main__':
    main()
