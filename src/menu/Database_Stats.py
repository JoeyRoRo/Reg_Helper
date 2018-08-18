#!/usr/bin/env python
from __future__ import print_function
import subprocess
import os
import time
import sys

# Set up Vendoring
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

# use the correct clear command depending on OS
if os.name == 'nt':
    CLEAR_CMD = 'cls'
else:
    CLEAR_CMD = 'clear'

short_name = 'Opt 2'
disp_name = 'Database Stats'
otype = 'Routine'
need = ['Where is the location of your Old Database file: ',
        'Where is the location of your New Database file: ']


def get_answers():
    """
    Gets the answers from the user. An empty answer from the user quits
    """
    answers = []
    while True:
        os.system(CLEAR_CMD)
        i = 0
        while i < len(need):
            ans = raw_input(need[i]).strip()

            # an empty answer quits
            if not ans:
                sys.exit(0)

            if validate_file_read(ans):
                answers.append(ans)
                i += 1
        break
    return answers


def run():
    hits = 0
    dups = {}

    answers = get_answers()

    read_file_for_dups(answers[0], dups)
    read_file_for_dups(answers[1], dups)

    output_to_file(answers)

    raw_input('\n\nSearch finished with '+str(hits) +
              ' results found. Please press enter to return.')


def output_to_file(answers):
    now = time.strftime("%d%b%Y-%H%M")
    path = os.getcwd()
    save_file = path+"\\Search_Results\\Database_Sumary_on_"+str(now)+'.txt'

    sys.stdout.write('\nWriting search hits to file...')
    with open(answers[0], 'r') as first_file:
        with open(answers[1], 'r') as second_file:
            with open(save_file, 'w') as output:
                output.write('Summary of search hits...\n')

                for z in sorted(dups, key=dups.__getitem__, reverse=True):
                    if dups[z] > 1:
                        output.write(str(z)+': '+str(dups[z])+'\n')

                output.write('\n\nHere are the search results...\n')

                for z in sorted(dups, key=dups.__getitem__, reverse=True):
                    found_lines = []
                    sesh = ''

                    if dups[z] > 1:
                        first_file.seek(0)
                        for _ in range(2):
                            next(first_file)
                        for line in first_file:
                            line1_split = line.split(',')
                            if str(z) in line:
                                if not sesh == line1_split[1]:
                                    sesh = line1_split[1]
                                    found_lines.append(line)

                        second_file.seek(0)
                        for _ in range(2):
                            next(second_file)
                        for line2 in second_file:
                            line2_split = line2.split(',')
                            if str(z) in line2:
                                if not sesh == line2_split[1]:
                                    sesh = line2_split[1]
                                    found_lines.append(line2)

                        output.write('\nFound '+str(z)+' with ' +
                                     str(dups[z])+' hits.\n')
                        for k in found_lines:
                            output.write(k)
                            sys.stdout.write('.')
                            hits += 1


def validate_file_read(f):
    """
    Validates the file given by the user exists and is able to be opened with read access

    Parameters
    ----------
    f : string
        a file path
    """
    try:
        open(f, 'r')
    except:
        print('error: unable to read file \'{}\'\n\
    please ensure the file exists and is readable\n'.format(f))
        return False
    return True


def read_file_for_dups(f, dups, special_fields=False):
    """
    Opens the file for reading. Reads each line into a dictionary. Counts how many times the line
    fragment has been used.

    Parameters
    ----------
    f: string
        The file to read
    dups: dict(string, int)
        The line segment as a string and it's occurrences
    special_fields: bool
        If True each line will be checked if it starts with 'Time' or 'Combined' and skip if so
    """
    with open(f, 'r') as log:
        # skip first two lines of second log
        for _ in range(2):
            next(log)

        for line in log:
            if special_fields and line.startswith('Time') or line.startswith('Combined'):
                pass

            line_split = line.split(',')

            check_and_add_segment(line_split[3], dups)
            check_and_add_segment(line_split[6], dups)


def check_and_add_segment(segment, dups):
    """
    Checks if the segment (key) is already in the dictionay, and increases the count (value) if so

    Parameters
    ----------
    segment: string
        The segment to check as the dictionary key
    dups: dict(string, int)
        The dictionary to check against
    """
    if segment and not segment in dups:
        dups.update({str(segment): 1})
    else:
        dups[segment] += 1
