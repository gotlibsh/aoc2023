from itertools import pairwise

def transpose(note):
    return [''.join(col) for col in zip(*note, strict=True)]

def get_notes(data):
    notes = data.split('\n\n')
    return [n.split('\n') for n in notes]

def find_row_reflection(note, skip=0):
    for i, (r1, r2) in enumerate(pairwise(note)):
        if skip == i+1:
            continue

        if r1 == r2:
            upper = reversed(note[:i])
            lower = note[i+2:]
            
            if all(ri == rj for ri, rj in zip(upper, lower)):
                return i + 1

    return 0

def find_col_reflection(note, skip=0):
    note_cols = transpose(note)

    for i, (c1, c2) in enumerate(pairwise(note_cols)):
        if skip == i+1:
            continue

        if c1 == c2:
            left = reversed(note_cols[:i])
            right = note_cols[i+2:]

            if all (ci == cj for ci, cj in zip(left, right)):
                return i + 1

    return 0

def find_smudge(note):
    opposite = {'.': '#', '#': '.'}
    r, c = find_row_reflection(note), find_col_reflection(note)

    for i,row in enumerate(note):
        for j,col in enumerate(row):
            before = row[:j]
            after = row[j+1:]
            opp = opposite[col]
            note[i] = before + opp + after

            cur_r, cur_c = find_row_reflection(note, skip=r), find_col_reflection(note, skip=c)

            if cur_r and r != cur_r:
                return note, cur_r * 100
            if cur_c and c != cur_c:
                return note, cur_c

            note[i] = row

    assert 0, 'could not find a smudge'

with open('../input/13.txt', 'r') as f:
    data = f.read()

notes = get_notes(data)
notes = [find_smudge(n) for n in notes]
print(sum(score for _,score in notes))
