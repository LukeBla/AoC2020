'''
Created on 24 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(24)

import numpy as np

class Tile(object):
    _tile_map = {}
    WHITE = 0
    BLACK = 1
    
    dir_map = {"e":np.array((1,0)),
                   "ne":np.array((0,1)),
                   "nw":np.array((-1,1)),
                   "w":np.array((-1,0)),
                   "sw":np.array((0,-1)),
                   "se":np.array((1,-1))}
    
    @staticmethod
    def parse_directions(directions):
        ret = []
        def get_next_direction(directions):
            for d in ["se", "sw", "ne", "nw", "w", "e"]:
                if directions.startswith(d):
                    directions = directions.replace(d, "", 1)
                    return(d, directions)
            raise RuntimeError(f"Count not parse string {directions}")
        while directions:
            (d, directions) = get_next_direction(directions)
            ret.append(d)
        return ret
                
    
    def __init__(self, coords):
        self.coords = coords
        self.colour = Tile.WHITE
        Tile._tile_map[coords] = self
    
    def add_neighbours(self):
        """
        Add in any neighbouring tiles that do not exist - only for black tiles
        """
        if self.colour == Tile.WHITE: return
        for dir in Tile.dir_map.keys():
            _ = self.tile_in_direction(dir)
    
    def set_should_switch(self):
        self.should_switch = False
        adjacent_colours = []
        for d in Tile.dir_map.keys():
            adjacent_tile = self.tile_in_direction(d, create_nonexistent=False)
            if adjacent_tile is None:
                adjacent_colours.append(Tile.WHITE)
            else:
                adjacent_colours.append(adjacent_tile.colour)
        num_adjacent_black = len([c for c in adjacent_colours if c == Tile.BLACK])
        if self.colour == Tile.BLACK:
            if num_adjacent_black == 0 or num_adjacent_black > 2:
                self.should_switch = True
        else:
            if num_adjacent_black == 2:
                self.should_switch = True
    
    def switch_colour(self):
        self.colour = 1 - self.colour
    
    def coord_in_direction(self, direction):
        return tuple(Tile.dir_map[direction] + self.coords)
    
    def tile_in_direction(self, direction, create_nonexistent=True):
        coords = self.coord_in_direction(direction)
        if coords in Tile._tile_map:
            tile = Tile._tile_map[coords]
        else:
            if create_nonexistent:
                tile = Tile(coords)
                Tile._tile_map[coords] = tile
            else:
                tile = None
        return tile
    
    def __str__(self):
        if self.colour == Tile.BLACK:
            col = "black"
        else:
            col = "white"
        return f"Tile {self.coords} - {col}"

def get_input(input_type):
    if input_type == "test1":
        ret = ["esew"]
    elif input_type == "test2":
        ret = ["nwwswee"]
    elif input_type == "test3":
        ret = ["sesenwnenenewseeswwswswwnenewsewsw",
        "neeenesenwnwwswnenewnwwsewnenwseswesw",
        "seswneswswsenwwnwse",
        "nwnwneseeswswnenewneswwnewseswneseene",
        "swweswneswnenwsewnwneneseenw",
        "eesenwseswswnenwswnwnwsewwnwsene",
        "sewnenenenesenwsewnenwwwse",
        "wenwwweseeeweswwwnwwe",
        "wsweesenenewnwwnwsenewsenwwsesesenwne",
        "neeswseenwwswnwswswnw",
        "nenwswwsewswnenenewsenwsenwnesesenew",
        "enewnwewneswsewnwswenweswnenwsenwsw",
        "sweneswneswneneenwnewenewwneswswnese",
        "swwesenesewenwneswnwwneseswwne",
        "enesenwswwswneneswsenwnewswseenwsese",
        "wnwnesenesenenwwnenwsewesewsesesew",
        "nenewswnwewswnenesenwnesewesw",
        "eneswnwswnwsenenwnwnwwseeswneewsenese",
        "neswnwewnwnwseenwseesewsenwsweewe",
        "wseweeenwnesenwwwswnew"]
    else:
        ret = []
        with open("input.txt") as f:
            for line in f:
                ret.append(line.strip())
    return ret

def run(input_type):
    Tile._tile_map = {}
    center = Tile((0,0))
    for chain in get_input(input_type):
        current = center
        for d in Tile.parse_directions(chain):
            next_tile = current.tile_in_direction(d)
            current = next_tile
        current.switch_colour()
    num_black = 0
    NUM_ROUNDS=100
    for _ in range(NUM_ROUNDS):
        # Add in any extra neighbours
        for t in list(Tile._tile_map.values()):
            t.add_neighbours()
        for t in list(Tile._tile_map.values()):
            t.set_should_switch()
        for t in Tile._tile_map.values():
            if t.should_switch:
                t.switch_colour()
    num_black = 0
    for t in Tile._tile_map.values():
        if t.colour == Tile.BLACK:
            num_black += 1
    print(f"{num_black} black tiles")
            
            