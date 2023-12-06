import re
from math import sqrt, ceil, floor

def ints(s: str):
    matches = re.findall('-?\d+', s)
    return [int(match) for match in matches]

def solve_inquality(a, b, c):
    # inequality: aX^2 + bX + c > 0
    # we want to transform the left-hand side to something like (x+m)^2
    # for that we use the complete-square technique
    right_hand = 0

    # move c to the right side
    right_hand = -c

    # isolate x^2, divide by a
    right_hand /= a
    b_new = b/a

    # we now have: x^2 + b_new*x > -c/a
    # we want to make it x^2 + 2x * (b_new/2) > -c/a
    b_const = b_new/2
    b_new = 2

    # we now have: x^2 b_new*x * b_const > -c/a
    # add b_const^2 to both sides
    right_hand += b_const**2

    # we now have: x^2 + b_new*x * b_const + b_const^2 > -c/a + b_const^2
    # so: (x + b_const)^2 = -c/a + b_const^2
    # sqrt both sides: x + b_const = +- sqrt(-c/a + b_const^2)
    # so: x = sqrt(-c/a + b_const^2) - b_const, -sqrt(-c/a + b_const^2) - b_const
    x1, x2 = sqrt(right_hand), -sqrt(right_hand)
    sol1, sol2 = x1 - b_const, x2 - b_const

    return sol1, sol2

with open('../input/6.txt', 'r') as f:
    lines = f.readlines()

times = ints(lines[0])
dist = ints(lines[1])
races = [(times[i], dist[i]) for i in range(len(times))]

# let x = race-time
# let y = race-distance
# let s = race-speed
# let t = race-travel-time
# let h = race-button-hold-time
# note that s = h
# note that t = x - h
#
# we want: s * t > y ==> h * (x - h) > y ==> -h^2 + xh - y > 0
# x and y are known constants, so we need to solve this inequality for h
# per race and then count how many integers are inside the interval

res = 1
for race in races:
    a, b, c = -1, race[0], -race[1]
    s1, s2 = solve_inquality(a,b,c)
    s = sorted([s1, s2])
    lower, upper = s

    if int(lower) == lower:
        lower += 1
    if int(upper) == upper:
        upper -= 1

    lower = ceil(lower)
    upper = floor(upper)

    res *= (upper - lower) + 1

print(res)
