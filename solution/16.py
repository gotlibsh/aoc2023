import re
from itertools import cycle
from functools import reduce
from operator import mul

with open('../input/8.txt', 'r') as f:
    lines = f.read().splitlines()

directions = lines[0]
nodes = lines[2:]

c = re.compile('(...) = \((...), (...)\)')

nodes = {
    (m := c.match(node)).group(1): (m.group(2), m.group(3))
    for node in nodes
}

def walk_multi(starts, nodes, directions):
    '''walk multiple start points, return a list of steps required for each starting point to reach the end.'''

    dir_to_idx = {'L': 0, 'R': 1}
    steps = 0
    res = []

    def step(start, direction):
        return nodes[start][dir_to_idx[direction]]

    for s in starts:
        dir_iter = cycle(directions)
        steps = 0

        while not s[-1] == 'Z':
            d = next(dir_iter)
            s = step(s, d)
            steps += 1

        res.append(steps)

    return res

def factor(n):
    '''factor n, returns a list of primes that make up n.'''

    factors = []

    while n > 1:
        for i in range(2, n+1):
            if n % i == 0:
                factors.append(i)
                n //= i
                break

    return factors

def lcm(nums):
    '''least common multiple, returns the LCM of all numbers in nums.'''

    all_factors = []

    for n in nums:
        factors = factor(n)

        for f in set(factors):
            gap = factors.count(f) - all_factors.count(f)
            if gap > 0:
                all_factors.extend([f] * gap)

    return reduce(mul, all_factors)

starts = [k for k in nodes.keys() if k.endswith('A')]
steps = walk_multi(starts, nodes, directions)

print(lcm(steps))
