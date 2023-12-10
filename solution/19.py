def find_start(sketch):
    index = ''.join(sketch).find('S')
    row, col = divmod(index, len(sketch[0]))

    return row, col

def calc_start_pipe(sketch, row, col):
    left = sketch[row][col-1]
    right = sketch[row][col+1]
    up = sketch[row-1][col]
    down = sketch[row+1][col]

    l = left in 'FL-'
    r = right in 'J7-'
    u = up in '7F|'
    d = down in 'JL|'

    if l and u:
        return 'J'
    if l and r:
        return '-'
    if l and d:
        return '7'
    if u and r:
        return 'L'
    if u and d:
        return '|'
    if r and d:
        return 'F'
    
    assert 0, 'start point is not on a cycle'

def step(sketch, row, col, prev):
    '''move one step, direction is based on the previous step.'''

    current = sketch[row][col]

    if prev is None:
        p_row, p_col = row, col
    else:
        p_row, p_col = prev

    match current:
        case '|':
            if p_row == row-1:
                return row+1, col
            else:
                return row-1, col
        case '-':
            if p_col == col-1:
                return row, col+1
            else:
                return row, col-1
        case 'L':
            if p_row == row-1:
                return row, col+1
            else:
                return row-1, col
        case 'J':
            if p_row == row-1:
                return row, col-1
            else:
                return row-1, col
        case '7':
            if p_row == row+1:
                return row, col-1
            else:
                return row+1, col
        case 'F':
            if p_row == row+1:
                return row, col+1
            else:
                return row+1, col
        case '.':
            raise ValueError('found a dot(.), out of circle')
        case _:
            raise ValueError(f'unidentified tile {current}')

def cycle_size(sketch, start_row, start_col):
    '''count the cycle size.'''

    p_row, p_col = start_row, start_col
    row, col = step(sketch, start_row, start_col, None)
    steps = 1

    while (start_row, start_col) != (row, col):
        row_tmp, col_tmp = row, col
        row, col = step(sketch, row, col, (p_row, p_col))
        p_row, p_col = row_tmp, col_tmp
        steps += 1

    return steps

with open('../input/10.txt', 'r') as f:
    sketch = f.read().splitlines()

# add a . frame
width = len(sketch[0])
sketch = ['.' * (width+2)] + [f'.{line}.' for line in sketch] + ['.' * (width+2)]

sr, sc = find_start(sketch)
start_pipe = calc_start_pipe(sketch, sr, sc)
sketch[sr] = sketch[sr].replace('S', start_pipe)

print(cycle_size(sketch, sr, sc) // 2)
