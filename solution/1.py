import string

s = 0

with open('../input/1.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    line = [c for c in line if c in string.digits]
    line = ''.join(line)
    num = line[0] + line[-1]
    s += int(num)

print(s)