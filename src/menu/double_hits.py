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

short_name = 'Opt 1'
disp_name = 'Check x2 logs for double hits'
otype = 'Routine'
need = ['Where is the location of your first log file: ',
        'Where is the location of your second log file: ']
answers = []
yes_found = []
found_first = []
found_second = []


def run():
    global answers, found_first, found_second
    answers = ['', '']
    found_first = []
    found_second = []
    yes_found = []
    while True:
        os.system(CLEAR_CMD)
        i = 0
        while i < len(need):
            ans = raw_input(need[i])

            if validate(ans):
                answers.append(ans)
                i += 1
        answers[0] = (answers[0])[1:-1]
        answers[1] = (answers[1])[1:-1]

        wait_timer('\nSearching your log files..')
        with open(answers[0], 'r') as log_file:
            with open(answers[1], 'r') as other_file:
                for line in log_file:
                    if line.startswith('Time') or line.startswith('Combined'):
                        pass
                    else:
                        sys.stdout.write('.')
                        line_split = line.split(',')

                        if (len(line_split) > 4):
                            #truth = False
                            for line2 in other_file:
                                truth = False
                                if line2.startswith('Time') or line2.startswith('Combined'):
                                    pass
                                else:

                                    # Can't get it to find line_split[3] in line2
                                    if line_split[3] in line2:
                                        raw_input('its in line2')
                                        if not line_split[3] == '':
                                            print(
                                                line_split[3]+' is in: \n'+line2)
                                            raw_input('Found one')
                                            truth = True
                                    if (line_split[6] in line2):
                                        if not line_split[6] == '':
                                            print(
                                                line_split[6]+' is in: \n'+line2)
                                            raw_input('Found one')
                                            truth = True
                                    if truth == True:
                                        raw_input('TRUE')

                                        sys.stdout.write('!')
                                        found_first.append(line)
                                        found_second.append(line2)

        if len(found_first) > 0:
            output_to_file()

        raw_input('\n\nSearch finished with '+str(len(found_first)) +
                  ' results found. Please press enter to return.')
        return


def output_to_file():
    now = time.strftime("%d%b%Y-%H%m")
    path = os.getcwd()
    save_file = path+"\\Search_Results\\Search_on_"+str(now)+'.txt'
    with open(save_file, 'w') as output:
        j = 0
        while j < len(found_first):
            output.write('Search hit!! \nFound in file: '+str(answers[0]) +
                         '.\n '+found_first[j]+'\nFound in file: '+str(answers[1]) +
                         '\n'+found_second[j]+'\n\n')
            j += 1


def validate(char):
    if char:
        return True
    return False

# this sections prints a wait timer


def wait_timer(what):
    sys.stdout.write(what+'..')
    i = 4
    while i > 0:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(.25)
        i -= 1
