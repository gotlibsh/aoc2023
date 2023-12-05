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

    def resolve(self, num):
        for dest, src, length in self._entries:
            if src <= num < src + length:
                return dest - src + num
            
        return num

    def resolve_reverse(self, num):
        for dest, src, length in self._entries:
            if dest <= num < dest + length:
                return num - dest + src

        return num

    def iter_sorted(self):
        # sort by destination (first item)
        s = sorted(self._entries)

        for item in s:
            yield item

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

map_chain = [seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_humid, humid_to_loc]

def resolve_map_chain(seed, chain):
    for m in chain:
        seed = m.resolve(seed)

    return seed

def resolve_map_chain_reverse(seed, chain):
    for m in reversed(chain):
        seed = m.resolve_reverse(seed)

    return seed

# Algorithm:
# - sort the final map humid-to-location by location in ascending order
# - starting from the lowest location, resolve in reverse the seed it is mapped to
# - check if that seed exists in one of the defined seed ranges, if so, print the location and exit
for dest, src, length in humid_to_loc.iter_sorted():
    for loc in range(dest, dest+length):
        seed = resolve_map_chain_reverse(loc, map_chain)

        if any(seed in seed_rng for seed_rng in seeds):
            print(loc)
            exit()

print('not found')
