def transpose(platform):
    return [''.join(col) for col in zip(*platform, strict=True)]

def rotate(platform):
    return [''.join(col) for col in zip(*reversed(platform))]

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

def spin_cycle(platform):
    # north, west, south, east

    # north
    platform = tilt_north(platform)

    # west, rotate clockwise and tilt north
    platform = rotate(platform)
    platform = tilt_north(platform)

    # south, rotate clockwise once again then tilt north
    platform = rotate(platform)
    platform = tilt_north(platform)

    # east, same
    platform = rotate(platform)
    platform = tilt_north(platform)

    return rotate(platform) # rotate back to original form

def calc_load(platform):
    length = len(platform)
    s = 0

    for i,row in enumerate(platform):
        s += (length-i) * row.count('O')

    return s

def plat_to_str(platform):
    return '\n'.join(platform)

def spin_x_cycles(platform, x):
    steps = 0
    visited = {} # maps each state (=spin) to the number of steps it takes getting there

    while (plat_str := plat_to_str(platform)) not in visited:
        visited[plat_str] = steps
        platform = spin_cycle(platform)
        steps += 1

    cycle_start = visited[plat_str]
    cycle_size = steps - cycle_start
    remaining = (x - cycle_start) % cycle_size

    for _ in range(remaining):
        platform = spin_cycle(platform)

    return platform

with open('../input/14.txt', 'r') as f:
    platform = f.read().splitlines()

platform = spin_x_cycles(platform, 1_000_000_000)
print(calc_load(platform))
