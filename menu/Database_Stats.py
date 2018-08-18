#!/usr/bin/env python
from __future__ import print_function
import subprocess, os, time, sys

short_name = 'Opt 2'
disp_name = 'Database Stats'
otype = 'Routine'
need = ['Where is the location of your Old Database file: ', \
        'Where is the location of your New Database file: ']
answers = []
dups = {}
hits=0

def run():
    global answers, dups, hits
    hits=0
    answers=[]
    dups={}

    while True:
        os.system('cls')
        answers=['','']
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
            with open(answers[1], 'r') as second_log:
                for _ in range(2): next(log_file)
                for line in log_file:
                    #if line.startswith('Time') or  line.startswith('Combined'):
                    #    pass
                    #else:
                    line_split = line.split(',')

                    if not line_split[3] in dups:
                        if (line_split[3] != ''):
                            dups.update({str(line_split[3]):1})
                    else: dups[line_split[3]] +=1

                    if not line_split[6] in dups:
                        if line_split[6] != '':
                            dups.update({str(line_split[6]):1})
                    else: dups[line_split[6]] +=1

                for _ in range(2): next(second_log)
                for line in second_log:
                    if line.startswith('Time') or  line.startswith('Combined'):
                        pass
                    else:
                        line_split = line.split(',')

                        if not line_split[3] in dups:
                            if (line_split[3] != ''):
                                dups.update({str(line_split[3]):1})
                        else: dups[line_split[3]] +=1

                        if not line_split[6] in dups:
                            if line_split[6] != '':
                                dups.update({str(line_split[6]):1})
                        else: dups[line_split[6]] +=1

# Where I tried to cut out dups that were equal to 1
#                del_one=''
#                for w in sorted(dups, key=dups.__getitem__):
#                    if not del_one == '':
#                        del dups[del_one]
#                        del_one=''
#                    if dups[w]==1:
#                        del_one=str(w)

        output_to_file()

        raw_input('\n\nSearch finished with '+str(hits)+ \
        ' results found. Please press enter to return.')
        return

def output_to_file():
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
                    if dups[z] > 1: output.write(str(z)+': '+str(dups[z])+'\n')

                output.write('\n\nHere are the search results...\n')


                for z in sorted(dups, key=dups.__getitem__, reverse=True):
                    found_lines=[]
                    sesh=''

                    if dups[z] > 1:
                        first_file.seek(0)
                        for _ in range(2): next(first_file)
                        for line in first_file:
                            line1_split=line.split(',')
                            if str(z) in line:
                                if not sesh == line1_split[1]:
                                    sesh=line1_split[1]
                                    found_lines.append(line)

                        second_file.seek(0)
                        for _ in range(2): next(second_file)
                        for line2 in second_file:
                            line2_split=line2.split(',')
                            if str(z) in line2:
                                if not sesh == line2_split[1]:
                                    sesh=line2_split[1]
                                    found_lines.append(line2)

                        output.write('\nFound '+str(z)+' with '+str(dups[z])+' hits.\n')
                        for k in found_lines:
                            output.write(k)
                            sys.stdout.write('.')
                            hits +=1


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
