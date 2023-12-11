from itertools import combinations

def get_galaxy_coords(image):
    res = []

    for i,row in enumerate(image):
        for j,col in enumerate(row):
            if col == '#':
                res.append((i,j))

    return res

def calc_galaxy_distance(empty_rows, empty_cols, g1, g2):
    lower, higher = sorted((g1, g2))
    left, right = sorted((g1, g2), key=lambda x: x[1])

    d = higher[0] - lower[0] + right[1] - left[1]

    sub_square_row_rng = range(lower[0]+1, higher[0])
    sub_square_col_rng = range(left[1]+1, right[1])

    empty = len(set(empty_rows).intersection(sub_square_row_rng))
    empty += len(set(empty_cols).intersection(sub_square_col_rng))

    return d + (1_000_000 - 1) * empty

def empty_indices(image):
    return [i for i,data in enumerate(image) if all(c == '.' for c in data)]

with open('../input/11.txt', 'r') as f:
    image = f.read().splitlines()

image_rows = image
image_cols = [''.join([image[row][col] for row in range(len(image))]) for col in range(len(image[0]))]
empty_rows = empty_indices(image_rows)
empty_cols = empty_indices(image_cols)

galaxies = get_galaxy_coords(image)
galaxy_pairs = combinations(galaxies, 2)
print(sum(calc_galaxy_distance(empty_rows, empty_cols, g1, g2) for g1, g2 in galaxy_pairs))
