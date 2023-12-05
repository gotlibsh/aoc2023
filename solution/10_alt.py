# Credits to Nico for the smart algorithm :)

import re

def ints(s: str):
    matches = re.findall('-?\d+', s)
    return [int(match) for match in matches]

def get_lines_by_phrase(lines, phrase):
    start = -1

    for i,line in enumerate(lines):
        if line.startswith(phrase):
            start = i+1
            continue

        if start != -1:
            if line == '\n':
                return lines[start:i]
            elif i == len(lines) - 1:
                return lines[start:]

def lines_to_ints(lines):
    return [ints(line) for line in lines]

class Map:
    def __init__(self, entries):
        self._entries = entries
        self._init_transformations()

    def _init_transformations(self):
        t = {}
        sorted_by_src = sorted(self._entries, key=lambda entry: entry[1])

        for dest, src, length in sorted_by_src:
            src_rng = range(src, src+length)
            dst_rng = range(dest, dest+length)
            t[src_rng] = dst_rng

        # init gaps
        srcs = list(t.keys())
        for r1, r2 in zip(srcs[:-1], srcs[1:]):
            gap = range(r1.stop, r2.start)
            if len(gap) > 0:
                t[gap] = gap

        # lowest interval gap [0, ...]
        srcs = list(t.keys())
        if srcs[0].start > 0:
            gap = range(0, min(r.start for r in t.keys()))
            t[gap] = gap

        self._transformations = t
        self._max = max(r.stop for r in t.values())

    def _get_mapping_with_edge(self, r: range):
        edge = range(r.stop, r.stop)

        # handle the case where the given range extends beyond any mapping
        if r.stop > self._max:
            edge = range(self._max, r.stop)

        t = {k:v for k,v in self._transformations.items()}
        t[edge] = edge

        return t

    def _intersection(self, r1: range, r2: range):
        return range(max(r1.start, r2.start), min(r1.stop, r2.stop))

    def _get_intersects(self, r: range):
        srcs = self._get_mapping_with_edge(r).keys()
        res = [self._intersection(r, rx) for rx in srcs]
        res = [r for r in res if len(r) > 0]

        return res

    def _transform(self, r: range):
        for src, dest in self._get_mapping_with_edge(r).items():
            if len(self._intersection(r, src)) > 0:
                offset = r.start - src.start

                return range(dest.start + offset, dest.start + offset + len(r))

    def get_transformations(self, r: range):
        intersects = self._get_intersects(r)

        return [self._transform(r) for r in intersects]


with open('../input/5.txt', 'r') as f:
    lines = f.readlines()

seeds = ints(lines[0])
seeds = [range(seeds[i], seeds[i]+seeds[i+1]) for i in range(0, len(seeds), 2)]
seed_to_soil   = Map(lines_to_ints(get_lines_by_phrase(lines, 'seed-to-soil map')))
soil_to_fert   = Map(lines_to_ints(get_lines_by_phrase(lines, 'soil-to-fertilizer map')))
fert_to_water  = Map(lines_to_ints(get_lines_by_phrase(lines, 'fertilizer-to-water map')))
water_to_light = Map(lines_to_ints(get_lines_by_phrase(lines, 'water-to-light map')))
light_to_temp  = Map(lines_to_ints(get_lines_by_phrase(lines, 'light-to-temperature map')))
temp_to_humid  = Map(lines_to_ints(get_lines_by_phrase(lines, 'temperature-to-humidity map')))
humid_to_loc   = Map(lines_to_ints(get_lines_by_phrase(lines, 'humidity-to-location map')))

chain = [seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_humid, humid_to_loc]
ranges = [set(seeds)] + [set() for _ in range(len(chain))]

for i,rng_list in enumerate(ranges[:-1]):
    while rng_list:
        rng = rng_list.pop()
        transforms = chain[i].get_transformations(rng)
        ranges[i+1].update(transforms)

print(min(r.start for r in ranges[-1]))
