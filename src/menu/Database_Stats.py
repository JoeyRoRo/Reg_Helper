#!/usr/bin/env python
from __future__ import print_function
import subprocess
import os
import time
import sys

if os.name == 'nt':
    CLEAR_CMD = 'cls'
else:
    CLEAR_CMD = 'clear'

short_name = 'Opt 2'
disp_name = 'Database Stats'
otype = 'Routine'
need = ['Where is the location of your Old Database file: ',
        'Where is the location of your New Database file: ']
dups = {}
hits = 0


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
    global dups, hits
    hits = 0
    dups = {}

    answers = get_answers()

    wait_timer('\nSearching your log files..')

    with open(answers[0], 'r') as log_file:
        with open(answers[1], 'r') as second_log:
            for _ in range(2):
                next(log_file)
            for line in log_file:
                # if line.startswith('Time') or  line.startswith('Combined'):
                #    pass
                # else:
                line_split = line.split(',')

                if not line_split[3] in dups:
                    if (line_split[3] != ''):
                        dups.update({str(line_split[3]): 1})
                else:
                    dups[line_split[3]] += 1

                if not line_split[6] in dups:
                    if line_split[6] != '':
                        dups.update({str(line_split[6]): 1})
                else:
                    dups[line_split[6]] += 1

            for _ in range(2):
                next(second_log)
            for line in second_log:
                if line.startswith('Time') or line.startswith('Combined'):
                    pass
                else:
                    line_split = line.split(',')

                    if not line_split[3] in dups:
                        if (line_split[3] != ''):
                            dups.update({str(line_split[3]): 1})
                    else:
                        dups[line_split[3]] += 1

                    if not line_split[6] in dups:
                        if line_split[6] != '':
                            dups.update({str(line_split[6]): 1})
                    else:
                        dups[line_split[6]] += 1

# Where I tried to cut out dups that were equal to 1
#                del_one=''
#                for w in sorted(dups, key=dups.__getitem__):
#                    if not del_one == '':
#                        del dups[del_one]
#                        del_one=''
#                    if dups[w]==1:
#                        del_one=str(w)

    output_to_file(answers)

    raw_input('\n\nSearch finished with '+str(hits) +
              ' results found. Please press enter to return.')


def output_to_file(answers):
    global hits
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


def wait_timer(what):
    """
    this sections prints a wait timer
    """
    sys.stdout.write(what+'..')
    i = 4
    while i > 0:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(.25)
        i -= 1
