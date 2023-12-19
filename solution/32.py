def travel_left(board, breadcrumb_board, position):
    row, col = position

    while board[row][col] in '.-':
        if '-' in breadcrumb_board[row][col]:
            return
        breadcrumb_board[row][col] += '-'
        col -= 1

    match board[row][col]:
        case '*':
            return
        case '/':
            travel_down(board, breadcrumb_board, (row+1, col))
        case '\\':
            travel_up(board, breadcrumb_board, (row-1, col))
        case '|':
            travel_down(board, breadcrumb_board, (row+1, col))
            travel_up(board, breadcrumb_board, (row-1, col))

    breadcrumb_board[row][col] += '#'

def travel_right(board, breadcrumb_board, position):
    row, col = position

    while board[row][col] in '.-':
        if '-' in breadcrumb_board[row][col]:
            return
        breadcrumb_board[row][col] += '-'
        col += 1

    match board[row][col]:
        case '*':
            return
        case '/':
            travel_up(board, breadcrumb_board, (row-1, col))
        case '\\':
            travel_down(board, breadcrumb_board, (row+1, col))
        case '|':
            travel_down(board, breadcrumb_board, (row+1, col))
            travel_up(board, breadcrumb_board, (row-1, col))

    breadcrumb_board[row][col] += '#'

def travel_up(board, breadcrumb_board, position):
    row, col = position

    while board[row][col] in '.|':
        if '|' in breadcrumb_board[row][col]:
            return
        breadcrumb_board[row][col] += '|'
        row -= 1

    match board[row][col]:
        case '*':
            return
        case '/':
            travel_right(board, breadcrumb_board, (row, col+1))
        case '\\':
            travel_left(board, breadcrumb_board, (row, col-1))
        case '-':
            travel_right(board, breadcrumb_board, (row, col+1))
            travel_left(board, breadcrumb_board, (row, col-1))

    breadcrumb_board[row][col] += '#'

def travel_down(board, breadcrumb_board, position):
    row, col = position

    while board[row][col] in '.|':
        if '|' in breadcrumb_board[row][col]:
            return
        breadcrumb_board[row][col] += '|'
        row += 1

    match board[row][col]:
        case '*':
            return
        case '/':
            travel_left(board, breadcrumb_board, (row, col-1))
        case '\\':
            travel_right(board, breadcrumb_board, (row, col+1))
        case '-':
            travel_right(board, breadcrumb_board, (row, col+1))
            travel_left(board, breadcrumb_board, (row, col-1))

    breadcrumb_board[row][col] += '#'

def count_energized(breadcrumbs):
    return sum((bool(tile) for line in breadcrumbs for tile in line))

def create_breadcrumbs(board):
    return [['' for _ in range(len(board[0]))] for _ in range(len(board))]

def find_max_config(board):
    m = 0
    rows = len(board) - 2
    cols = len(board[0]) - 2

    for i in range(1, cols+1):
        breadcrumbs = create_breadcrumbs(board)
        travel_down(board, breadcrumbs, (1, i))
        e = count_energized(breadcrumbs)

        if e > m:
            m = e

        breadcrumbs = create_breadcrumbs(board)
        travel_up(board, breadcrumbs, (len(board)-2, i))
        e = count_energized(breadcrumbs)

        if e > m:
            m = e
    
    for i in range(1, rows+1):
        breadcrumbs = create_breadcrumbs(board)
        travel_right(board, breadcrumbs, (i, 1))
        e = count_energized(breadcrumbs)

        if e > m:
            m = e

        breadcrumbs = create_breadcrumbs(board)
        travel_left(board, breadcrumbs, (i, len(board[0])-2))
        e = count_energized(breadcrumbs)

        if e > m:
            m = e
    
    return m

with open('../input/16.txt', 'r') as f:
    contraption = f.read().splitlines()

# add a * frame
contraption = ['*' * (len(contraption[0]) + 2)] + [f'*{l}*' for l in contraption] + ['*' * (len(contraption) + 2)]

print(find_max_config(contraption))
