import re
from itertools import product, repeat

class Record:
    def __init__(self, s: str):
        self._record, self._groups = s.split(' ')
        self._groups = [int(x) for x in self._groups.split(',')]
        self._unknowns = [i for i in range(len(s)) if s[i] == '?']

    def iter_arrangements(self):
        s = list(self._record)
        unknowns = self._unknowns
        num_unknown = len(unknowns)
        iterator = product(*repeat((0,1), num_unknown))

        for i in iterator:
            for j,x in enumerate(i):
                if x:
                    s[unknowns[j]] = '#'
                else:
                    s[unknowns[j]] = '.'

            yield ''.join(s)

    def match(self, arrangement):
        arng_groups = re.findall('#+', arrangement)
        arng_groups = [len(group) for group in arng_groups]

        return arng_groups == self._groups

    def count_possible_arrangements(self):
        s = 0

        for arng in self.iter_arrangements():
            if self.match(arng):
                s += 1

        return s

with open('../input/12.txt', 'r') as f:
    records = f.read().splitlines()

records = [Record(r) for r in records]
print(sum(r.count_possible_arrangements() for r in records))
