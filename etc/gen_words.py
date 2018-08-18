#!/usr/bin/env python

import progressbar
import random

MAX = 10000
words = []
weights = [50] * 2 + [30] * 2 + [10] * 4 + \
    [5] * 7 + [3] * 20 + [2] * 20 + [1] * 45

print('Picking random words...')
with open('american-english', 'r') as w:
    with progressbar.ProgressBar(max_value=MAX) as bar:
        i = 0
        while i < MAX:
            bar.update(i)
            w.seek(0)
            r_line = random.randint(1, 100000)
            for j, line in enumerate(w):
                if j == r_line:
                    for _ in range(0, random.choice(weights)):
                        words.append(line)
                        i += 1
                    break

print('Writing words...')
with open('words', 'w') as f:
    while words:
        f.write(words.pop(random.randint(0, len(words)-1)))
