class Game:
    def __init__(self, s: str) -> None:
        self._id = 0
        self._sets = []

        # game string format:
        # Game <id>: <x1> <color_x1>, <x2> <color_x2>, ...; <y1> <color_y1>, <y2> <color_y2>; ...
        pre_colon, _, post_colon = s.partition(':')

        # game id
        self._id = int(pre_colon.split()[-1])

        # game sets
        self._sets = [s.strip() for s in post_colon.split(';')]
        self._sets = [self._parse_set(s.strip()) for s in self._sets]

    def _parse_set(self, s: str):
        _set = {'red': 0, 'green': 0, 'blue': 0}

        # set string format:
        # <x1> <color_x1>, <x2> <color_x2>, ...
        s = [unit.strip() for unit in s.split(',')]

        for unit in s:
            num, color = unit.split()
            _set[color] = int(num)

        return _set

    def is_bag_possible(self, bag):
        return all(
            s['red'] <= bag['red'] and s['green'] <= bag['green'] and s['blue'] <= bag['blue']
            for s in self._sets
        )

with open('../input/2.txt', 'r') as f:
    lines = f.readlines()

games = [Game(line) for line in lines]

s = sum(game._id for game in games if game.is_bag_possible({'red': 12, 'green': 13, 'blue': 14}))
print(s)
