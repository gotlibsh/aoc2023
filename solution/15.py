import re
from itertools import cycle

with open('../input/8.txt', 'r') as f:
    lines = f.read().splitlines()

directions = lines[0]
nodes = lines[2:]

c = re.compile('(...) = \((...), (...)\)')

nodes = {
    (m := c.match(node)).group(1): (m.group(2), m.group(3))
    for node in nodes
}

def walk(start, end, nodes, directions):
    '''walk on nodes from start to end following the directions, returns the number of steps.'''

    dir_iter = cycle(directions)
    dir_to_idx = {'L': 0, 'R': 1}
    steps = 0

    while start != end:
        start = nodes[start][dir_to_idx[next(dir_iter)]]
        steps += 1

    return steps

print(walk('AAA', 'ZZZ', nodes, directions))
