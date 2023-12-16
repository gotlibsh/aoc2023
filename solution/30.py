class Box:
    def __init__(self, id) -> None:
        self._id = id
        self._lenses = {}   # map label to focal length, keeps insertion order

    def dash(self, label):
        self._lenses.pop(label, None)

    def equal(self, label, focal_length):
        self._lenses[label] = focal_length

    def focusing_power(self):
        s = 0

        for slot, focal_length in enumerate(self._lenses.values(), start=1):
            s += slot * (self._id+1) * focal_length

        return s

def hash(s: str):
    h = 0

    for c in s:
        h += ord(c)
        h *= 17
        h %= 256

    return h

def HASHMAP_procedure(init_seq, boxes):
    for step in init_seq:
        if '-' in step:
            label = step.partition('-')[0]
            action = '-'
        elif '=' in step:
            label, _, focal_length = step.partition('=')
            action = '='
        else:
            assert 0, 'invalid action'

        box_id = hash(label)
        box = boxes[box_id]

        if action == '-':
            box.dash(label)
        else:
            box.equal(label, int(focal_length))

with open('../input/15.txt', 'r') as f:
    init_seq = f.read().split(',')

boxes = [Box(i) for i in range(256)]
HASHMAP_procedure(init_seq, boxes)
print(sum(b.focusing_power() for b in boxes))
