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

# Vendored deps
import clapp

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


def run():
    answers = get_answers()
    _run(answers)


def _run(answers):
    dups = {}

    read_file_for_dups(answers[0], dups)
    read_file_for_dups(answers[1], dups, special_fields=True)

    hits = output_to_file(answers, dups)

    print('\n\nSearch finished with {} results found.'.format(hits))

    # We don't want to pause if we running in script mode
    if __name__ != '__main__':
        raw_input('Please press enter to return.')


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


def validate_new_db(ctx):
    validate_file_read(ctx['newdb'])


def validate_old_db(ctx):
    validate_file_read(ctx['olddb'])


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

    print('Reading database \'{}\'...'.format(f))

    with open(f, 'r') as log:
        # skip first two lines of second log
        for _ in range(2):
            next(log)

        for line in log:
            if special_fields and line.startswith('Time') or line.startswith('Combined'):
                continue

            line_split = line.split(',')

            check_and_add_segment(line_split[3], line, dups)
            check_and_add_segment(line_split[6], line, dups)


def check_and_add_segment(segment, line, dups):
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
        dups[segment] = (1, [line])
    else:
        occs = dups[segment][0] + 1
        lines = dups[segment][1]
        lines.append(line)
        dups[segment] = (occs, lines)


def output_to_file(answers, dups):
    now = time.strftime("%d%b%Y-%H%M")
    path = os.getcwd()
    path = os.path.join(path, "Search_Results")
    save_file = os.path.join(
        path, 'Database_Sumary_on_{}.txt'.format(now))

    total_hits = 0

    print('Trimming dups...')
    # make a new dict with only the items whos value is greater than 1
    trimmed = {k: v for k, v in dups.iteritems() if k and v[0] > 1}

    print('Writing summary search hits to file...')

    with open(save_file, 'w') as output:
        output.write('Summary of search hits...\n')

        s_trimmed = sorted(
            trimmed, key=trimmed.__getitem__, reverse=True)

        for z in s_trimmed:
            output.write('{}: {}\n'.format(z, dups[z][0]))

        print('Writing full search hits to file...')
        output.write('\n\nHere are the search results...\n')

        for z in s_trimmed:
            found_lines = []
            sesh_ids = set()
            hits = 0

            find_lines(trimmed, z, sesh_ids, found_lines)
            find_lines(trimmed, z, sesh_ids, found_lines)

            output.write(
                '\nFound {} with {} hits.\n'.format(z, trimmed[z][0]))

            for k in found_lines:
                output.write(k)
                hits += 1
            total_hits += hits
    return total_hits


def find_lines(d, z, sesh_ids, found_lines):
    """
    Checks the entire file for lines matching the segment and adds lines with unique session ids

    Parameters
    ----------
    d: dict(string, (int, list(string)))
        The dict to check
    z: string
        The segment to check for
    sesh_ids: list(string)
        A list of session ids that have already been found and used
    found_lines: list(string)
        A list of found lines to append to
    """
    lines = d[z][1]
    for line in lines:
        line1_split = line.split(',')
        sesh = line1_split[1]
        if sesh not in sesh_ids:
            sesh_ids.add(sesh)
            found_lines.append(line)


def main(ctx):
    answers = [ctx['olddb'], ctx['newdb']]
    _run(answers)


def build_app():
    app = clapp.App('db_stats')
    app.version = '1.0'
    app.about = 'Does some string finding on database files'
    app.author = 'JoeJoeJoey <joejoejoey13@gmail.com>'
    app.main = main

    arg1 = clapp.Arg('olddb')
    arg1.index = 1
    arg1.help = 'The old database'
    arg1.required = True
    arg1.action = validate_old_db

    arg2 = clapp.Arg('newdb')
    arg2.index = 2
    arg2.help = 'The new database'
    arg2.required = True
    arg2.action = validate_new_db

    app.add_args([arg1, arg2])

    return app


if __name__ == '__main__':
    app = build_app()
    app.start()
    sys.exit(0)
