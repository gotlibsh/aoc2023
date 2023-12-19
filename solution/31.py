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

with open('../input/16.txt', 'r') as f:
    contraption = f.read().splitlines()

# add a * frame
contraption = ['*' * (len(contraption[0]) + 2)] + [f'*{l}*' for l in contraption] + ['*' * (len(contraption) + 2)]
breadcrumbs = [['' for _ in range(len(contraption[0]))] for _ in range(len(contraption))]
travel_right(contraption, breadcrumbs, (1,1))
print(sum((bool(tile) for line in breadcrumbs for tile in line)))
