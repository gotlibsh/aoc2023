from itertools import chain

class Line():
    def __init__(self, line: str) -> None:
        self._line = line

    def iter_nums(self):
        '''Iterates over (num, start, end) tuples that hold the number,
        start index and end index of the number in that line.'''

        idx = 0

        while idx < len(self._line):
            if self._line[idx].isdigit():
                start = idx

                while self._line[idx].isdigit():
                    idx += 1

                end = idx

                yield int(self._line[start:end]), start, end
            else:
                idx += 1

    def iter_stars(self):
        '''Iterate over all indices of star symbols in the line.'''

        for i,s in enumerate(self._line):
            if s == '*':
                yield i


with open('../input/3.txt', 'r') as f:
    scheme = f.read().split()

# add a period frame
width = len(scheme[0])
scheme = ['.' * (width + 2)] + [f'.{line}.' for line in scheme] + ['.' * (width + 2)]
lines = [Line(line) for line in scheme]
s = 0

for row,l in enumerate(lines):
    for star_idx in l.iter_stars():
        nums_up = lines[row-1].iter_nums()
        nums_cu = lines[row].iter_nums()
        nums_do = lines[row+1].iter_nums()
        num_neighbours = []

        for num, start, end in chain(nums_up, nums_cu, nums_do):
            if (start - 1) <= star_idx <= end:
                num_neighbours.append(num)

        if len(num_neighbours) == 2:
            s += num_neighbours[0] * num_neighbours[1]

print(s)
