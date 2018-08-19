#!/usr/bin/env python

# Set up Vendoring
import os
import sys
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')
sys.path.append(vendor_dir)

# Std Deps
import random

# Vendored Deps
import progressbar
import clapp

weights = [50] * 1 + [30] * 1 + [20] * 4 + [10] * 20 + \
    [5] * 70 + [3] * 200 + [2] * 200 + [1] * 450
spec_words_weights = [False] * 99 + [True]
sesh_id_weights = [123456] * 33 + [789123] * 33 + [456789] * 34
USE_SPECIAL = False


def use_special(context):
    global USE_SPECIAL
    USE_SPECIAL = True


def main(ctx):
    words = []
    print('Picking random words...')
    # If the user wants 1000 lines, we actually need about
    # 2,000 words since each line has 2 words
    MAX = ctx['lines'] * 2
    with open(ctx['word_file'], 'r') as w:
        for i, _ in enumerate(w):
            pass
        word_line_count = i + 1
        w.seek(0)
        with progressbar.ProgressBar(max_value=MAX) as bar:
            i = 0
            while i < MAX:
                bar.update(i)
                w.seek(0)
                r_line = random.randint(1, word_line_count)
                for j, line in enumerate(w):
                    if j == r_line:
                        words.append(line.strip())
                        i += 1
                        break

    # Now we have a bunch of random words
    # we need to duplicate some of them
    for i in range(len(words)/3):
        word = words[i]
        for _ in range(random.choice(weights)):
            words.append(word)

    testdb = ctx['output'][0]
    print('Writing {}...'.format(testdb))
    with open(testdb, 'w') as f:
        f.write('header line 1 which is ignored by scripts\n')
        f.write('header line 2 which is ignored by scripts\n')
        i = 0
        while i < ctx['lines']:
            if USE_SPECIAL and random.choice(spec_words_weights):
                f.write('Time,a,{},c,{},e,f,{},h,i\n'.format(
                    random.choice(sesh_id_weights),
                    words.pop(random.randint(0, len(words)-1)),
                    words.pop(random.randint(0, len(words)-1))))
            else:
                f.write('a,{},c,{},e,f,{},h,i\n'.format(
                    random.choice(sesh_id_weights),
                    words.pop(random.randint(0, len(words)-1)),
                    words.pop(random.randint(0, len(words)-1))))
            i += 1
    return 0


def build_app():
    app = clapp.App('gen_testdb')
    app.version = '1.0'
    app.about = 'Generates some test databases for Reg_Help'
    app.author = 'Kevin K. <kbknapp@gmail.com>'
    app.main = main

    arg1 = clapp.Arg('lines')
    arg1.short = '-l'
    arg1.long = '--lines'
    arg1.args_taken = 1
    arg1.help = 'How many lines to generate'
    arg1.default = 10000

    arg2 = clapp.Arg('word_file')
    arg2.index = 1
    arg2.help = 'The word file to use as dummy data'
    arg2.default = 'words.txt'
    arg2.required = True

    arg3 = clapp.Arg('spec-fields')
    arg3.short = '-s'
    arg3.long = '--special-fields'
    arg3.help = 'Should data randomly include lines starting with "Combined" or "Time"?'
    arg3.action = use_special

    arg4 = clapp.Arg('output')
    arg4.short = '-o'
    arg4.long = '--output'
    arg4.args_taken = 1
    arg4.help = 'The file to write the results to'
    arg4.required = True

    app.add_args([arg1, arg2, arg3, arg4])

    return app


if __name__ == '__main__':
    app = build_app()
    app.start()
    sys.exit(0)
