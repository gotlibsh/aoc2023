nums = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6,
        'seven': 7, 'eight': 8, 'nine': 9, **{n:int(n) for n in '123456789'}}

def find_first_num(s: str):
    idx = len(s)
    length = 0

    for n in nums:
        i = s.find(n)
        if i >= 0 and i < idx:
            idx = i
            length = len(n)
    
    num = s[idx: idx+length]
    return nums[num]

def find_last_num(s: str):
    ridx = -1
    rlength = 0

    for n in nums:
        ri = s.rfind(n)
        if ri >= 0 and ri > ridx:
            ridx = ri
            rlength = len(n)

    num = s[ridx: ridx+rlength]
    return nums[num]

s = 0

with open('../input/1.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    first, last = find_first_num(line), find_last_num(line)
    num = int(f'{first}{last}')
    s += num

print(s)