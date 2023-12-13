from itertools import pairwise

def transpose(note):
    return [''.join(col) for col in zip(*note, strict=True)]

def get_notes(data):
    notes = data.split('\n\n')
    return [n.split('\n') for n in notes]

def find_row_reflection(note):
    for i, (r1, r2) in enumerate(pairwise(note)):
        if r1 == r2:
            upper = reversed(note[:i])
            lower = note[i+2:]
            
            if all(ri == rj for ri, rj in zip(upper, lower)):
                return i + 1

    return 0

def find_col_reflection(note):
    note_cols = transpose(note)

    for i, (c1, c2) in enumerate(pairwise(note_cols)):
        if c1 == c2:
            left = reversed(note_cols[:i])
            right = note_cols[i+2:]

            if all (ci == cj for ci, cj in zip(left, right)):
                return i + 1

    return 0

def summarize(notes):
    s = 0

    for note in notes:
        if (cr := find_col_reflection(note)) > 0:
            s += cr
        elif (rr := find_row_reflection(note)) > 0:
            s += 100 * rr

    return s

with open('../input/13.txt', 'r') as f:
    data = f.read()

notes = get_notes(data)
print(summarize(notes))
