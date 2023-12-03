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


def get_neighbours(row, start_col, end_col, scheme):
    return [
        scheme[row-1][start_col-1],
        scheme[row-1][start_col:end_col],
        scheme[row-1][end_col],
        scheme[row][start_col-1],
        scheme[row][end_col],
        scheme[row+1][start_col-1],
        scheme[row+1][start_col:end_col],
        scheme[row+1][end_col],
    ]

with open('../input/3.txt', 'r') as f:
    scheme = f.read().split()

# add a period frame
width = len(scheme[0])
scheme = ['.' * (width + 2)] + [f'.{line}.' for line in scheme] + ['.' * (width + 2)]
lines = [Line(line) for line in scheme]
s = 0

for i,l in enumerate(lines):
    for num, start, end in l.iter_nums():
        neighbours = get_neighbours(i, start, end, scheme)

        # check if any neighbour is not all dots
        if any(neighbour for neighbour in neighbours if not all(c == '.' for c in neighbour)):
            s += num

print(s)
