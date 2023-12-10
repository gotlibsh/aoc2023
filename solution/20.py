from itertools import repeat

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

def build_cycle(sketch, start_row, start_col):
    '''return a clean board with only the cycle pipes on it.'''

    width = len(sketch[0])
    height = len(sketch)
    board = [['.' for _ in range(width)] for _ in range(height)]

    board[start_row][start_col] = sketch[start_row][start_col]

    p_row, p_col = start_row, start_col
    row, col = step(sketch, start_row, start_col, None)

    while (start_row, start_col) != (row, col):
        board[row][col] = sketch[row][col]
        row_tmp, col_tmp = row, col
        row, col = step(sketch, row, col, (p_row, p_col))
        p_row, p_col = row_tmp, col_tmp

    return board

def count(iterable, wall, skip, smooth):
    '''count how many walls are in the given iterable while smoothing out curved walls.
    for example:
        when counting up/down walls of type -, a 7 followed by an L counts as a single - because it's a curved wall going from west to east,
        similarly, when counting left/right walls of type |, an F followed by a J counts as a single | because it's a curved wall going from north to south.'''

    count = iterable.count(wall)
    it = iter(iterable)

    while c := next(it, None):
        if c in smooth:
            orig = c
            c = next(it)
            while c == skip:
                c = next(it)
            if c == smooth[orig]:
                count += 1
    
    return count

def count_sides(board_rows, board_cols, row, col):
    '''counts how many walls position (row, col) is sorrounded by, considering only walls opposite to the direction.'''

    left = board_rows[row][:col]
    left = count(left, '|', '-', {'F': 'J', 'L': '7'})

    right = board_rows[row][col+1:]
    right = count(right, '|', '-', {'F': 'J', 'L': '7'})

    above = board_cols[col][:row]
    above = count(above, '-', '|', {'7': 'L', 'F': 'J'})

    below = board_cols[col][row+1:]
    below = count(below, '-', '|', {'7': 'L', 'F': 'J'})

    return left, right, above, below

def calc_area(board_rows, board_cols):
    '''calculates the area withing the cycle.'''

    area = 0

    for i in range(len(board_rows)):
        for j in range(len(board_cols)):
            if board_rows[i][j] != '.':
                continue

            left, right, above, below = count_sides(board_rows, board_cols, i, j)

            if left % 2 == 1 and right % 2 == 1 and above % 2 == 1 and below % 2 == 1:
                area += 1

    return area

with open('../input/10.txt', 'r') as f:
    sketch = f.read().splitlines()

# add a . frame
width = len(sketch[0])
sketch = ['.' * (width+2)] + [f'.{line}.' for line in sketch] + ['.' * (width+2)]

sr, sc = find_start(sketch)
start_pipe = calc_start_pipe(sketch, sr, sc)
sketch[sr] = sketch[sr].replace('S', start_pipe)

cycle = build_cycle(sketch, sr, sc)
board_rows = cycle
board_cols = [[r[col] for r in board_rows] for col in range(len(board_rows[0]))]

# observation:
# each tile on the board is inside the cycle, if and only if, for each of its sides (left, right, up, down)
# the number of walls on that side is odd.
# algorithm:
# based on the above, iterate over all tiles and sum up only tiles that meet the observed condition.

print(calc_area(board_rows, board_cols))
