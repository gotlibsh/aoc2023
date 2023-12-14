def transpose(platform):
    return [''.join(col) for col in zip(*platform, strict=True)]

def tilt_north(platform):
    def new_position(new_col, index):
        for i in range(index-1, -1, -1):
            if new_col[i] in 'O#':
                return i+1
            
        return 0

    platform_cols = transpose(platform)
    res = []

    for col in platform_cols:
        new_col = [c if c == '#' else '.' for c in col]

        for i,tile in enumerate(col):
            if tile != 'O':
                continue

            new_pos = new_position(new_col, i)
            new_col[new_pos] = 'O'

        res.append(new_col)

    return transpose(res)

def calc_load(platform):
    length = len(platform)
    s = 0

    for i,row in enumerate(platform):
        s += (length-i) * row.count('O')

    return s

with open('../input/14.txt', 'r') as f:
    platform = f.read().splitlines()

platform = tilt_north(platform)
print(calc_load(platform))
