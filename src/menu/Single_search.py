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

short_name = 'Opt 3'
disp_name = 'Single search'
otype = 'Routine'
need = ['What do you want to search for: ',
        'Drag and drop a directory you want to search in: ']
answers = []
dups = {}


def run():
    global answers, dups
    answers = []
    dups = {}

    while True:
        os.system(CLEAR_CMD)
        i = 0
        while i < len(need):
            ans = raw_input(need[i])

            if validate(ans):
                answers.append(ans)
                i += 1
        answers[1] = (answers[1])[1:-1]

        wait_timer('\nSearching your in your files..')

        files = os.listdir(answers[1])
        for x in files:
            if os.path.isfile(answers[1]+'\\'+str(x)):
                with open(answers[1]+'\\'+str(x), 'r') as log_file:
                    for line in log_file:
                        if answers[0] in line:
                            dups.update({str(x): line})

        output_to_file()

        raw_input('\n\nSearch finished with '+str(len(dups)) +
                  ' results found. Please press enter to return.')
        return


def output_to_file():
    now = time.strftime("%d%b%Y-%H%m")
    path = os.getcwd()
    save_file = path+"\\Search_Results\\Single_Search_on_"+str(now)+'.txt'

    sys.stdout.write('\nWriting search hits to file...')
    with open(save_file, 'w') as output:
        output.write('Search results for '+answers[0]+' in the ' +
                     'directory of '+answers[1]+'.\n')
        j = ''
        for x, y in dups.iteritems():
            if x != j:
                output.write('\nSearches found in file: '+str(x)+'.\n')
            output.write(str(y))
            sys.stdout.write('.')
            j = x


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
