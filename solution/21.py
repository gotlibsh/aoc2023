from itertools import combinations

def exapnd(image):
    tmp_image = []
    new_image = []

    # expand columns
    for j in range(len(image[0])):
        col = [image[row][j] for row in range(len(image))]
        if all(c == '.' for c in col):
            tmp_image.extend([col, col])
        else:
            tmp_image.append(col)

    # convert columns to rows
    tmp_image = [
        ''.join([tmp_image[col][row] for col in range(len(tmp_image))])
        for row in range(len(image))
    ]

    # expand rows
    for row in tmp_image:
        if all(c == '.' for c in row):
            new_image.extend([row, row])
        else:
            new_image.append(row)

    return new_image

def get_galaxy_coords(image):
    res = []

    for i,row in enumerate(image):
        for j,col in enumerate(row):
            if col == '#':
                res.append((i,j))

    return res

def calc_galaxy_distance(g1, g2):
    lower, higher = sorted((g1, g2))
    left, right = sorted((g1, g2), key=lambda x: x[1])

    return higher[0] - lower[0] + right[1] - left[1]

with open('../input/11.txt', 'r') as f:
    image = f.read().splitlines()

image = exapnd(image)
print(sum(calc_galaxy_distance(g1, g2) for g1, g2 in combinations(get_galaxy_coords(image), 2)))
