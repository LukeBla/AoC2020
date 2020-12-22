'''
Created on 20 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(20)

import numpy as np
import re

class Tile(object):
    
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    
    def __init__(self, _id, tile):
        self.id = _id
        self.tile = tile
        self.unordered_borders = [tile[0,:], tile[-1,:], tile[:,0], tile[:, -1]]
        self.ordered_borders = [None] * 4
        self.unordered_neighbours = []
        self.ordered_neighbours = [None] * 4
        self.position = None

    def matches_border(self, border):
        if any([(border == b).all() for b in self.unordered_borders]):
            return True
        if any([(border[:: -1] == b).all() for b in self.unordered_borders]):
            return True
        return False
    
    def num_neighbours(self):
        n = len([x for x in self.unordered_neighbours if x is not None])
        if n == 0:
            raise RuntimeError(f"No neighbours set yet for id {self.id}")
        return n
        
    def add_neighbour(self, _id):
        if _id not in self.unordered_neighbours:
            self.unordered_neighbours.append(_id)
            
    def set_position(self, x, y):
        self.position = (x, y)
        
    def get_position(self):
        return self.position

def get_input(input_type):
    def _get_tile(fh):
        try:
            line = next(fh).strip()
        except StopIteration:
            return None
        m = re.match("Tile ([0-9]+):", line)
        if m is None:
            raise RuntimeError(f"Cannot match line {line} to tile header")
        _id = int(m.groups()[0])
        ret = []
        while True:
            try:
                line = next(fh).strip()
            except StopIteration:
                line = ""
            if line == "":
                return Tile(_id, np.array(ret))
            ret.append(list(line))
        
    if input_type == "test":
        input_file = "test_input.txt"
    else:
        input_file = "input.txt"
    tiles = {}
    with open(input_file) as f:
        while True:
            tile = _get_tile(f)
            if tile is None:
                return tiles
            else:
                tiles[tile.id] = tile

def get_corners(tile_dict):
    corners = []
    for tile in tile_dict.values():
        if tile.num_neighbours() == 2:
            corners.append(tile)
    return corners

def run(input_type):
    tile_dict = get_input(input_type)
    for (_id, tile) in tile_dict.items():
        other_tiles = list(filter(lambda x: x[0] != _id, tile_dict.items()))
        for (other_id, other_tile) in other_tiles:
            if any(other_tile.matches_border(border) for border in tile.unordered_borders):
                tile.add_neighbour(other_id)
                other_tile.add_neighbour(_id)
    corners = get_corners(tile_dict)
    corner_prod = np.prod(np.array([t.id for t in corners], dtype="int64"))
    print(f"Corner product: {corner_prod}")
        