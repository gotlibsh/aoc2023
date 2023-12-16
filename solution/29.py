def hash(s: str):
    h = 0

    for c in s:
        h += ord(c)
        h *= 17
        h %= 256

    return h

with open('../input/15.txt', 'r') as f:
    init_seq = f.read().split(',')

print(sum(hash(s) for s in init_seq))
