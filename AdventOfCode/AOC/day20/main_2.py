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
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    locations = [LEFT, TOP, RIGHT, BOTTOM]
    
    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    
    HORIZONTAL = 0
    VERTICAL = 1
    
    SAME_DIRECTION = 0
    OPPOSITE_DIRECTION = 1
    
    def __init__(self, _id, tile):
        self.id = _id
        self.tile = tile
        self.unordered_neighbours = []
        self.neighbours = [None] * 4
        self.position = None

    @property
    def borders(self):
        return [self.tile[:, 0], self.tile[0, :], self.tile[:, -1], self.tile[-1, :]]


    def matches_border(self, border, location, check_direction=True):
        if (border == self.borders[location]).all():
            return True
        if check_direction: return False
        return (border[::-1] == self.borders[location]).all()

    def get_location(self, border):
        # returns tuple (location, direction) - direction = -1 if reversed
        if not self.matches_any_border(border):
            raise RuntimeError("Border does not match at all")
        for loc in self.locations:
            if self.matches_border(border, loc):
                return (loc, Tile.SAME_DIRECTION)
            if self.matches_border(border, loc, check_direction=False):
                return (loc, Tile.OPPOSITE_DIRECTION)
        raise RuntimeError("Could not get border location")

    def matches_any_border(self, border):
        if any([(border == b).all() for b in self.borders]):
            return True
        if any([(border[:: -1] == b).all() for b in self.borders]):
            return True
        return False
    
    def _flip(self, axis):
        if axis == Tile.VERTICAL:
            self.tile = np.flip(self.tile, axis=1)
        elif axis == Tile.HORIZONTAL:
            self.tile = np.flip(self.tile, axis=0)
        return self
    
    def _rotate(self, direction, angle):
        if direction == Tile.CLOCKWISE:
            angle = 360 - angle
        for _ in range(angle//90):
            self.tile = np.rot90(self.tile)
        return self
    
    def set_border(self, border, desired_loc):
        """
        Rotate/flip to match border at given location
        """
        if not self.matches_any_border(border):
            raise RuntimeError("Border does not exist")
        if self.matches_border(border, desired_loc):
            # Already matches
            return
        elif self.matches_border(border, desired_loc, check_direction=False):
            # Simple flip
            if desired_loc in [Tile.LEFT, Tile.RIGHT]:
                self._flip(Tile.HORIZONTAL)
            else:
                self._flip(Tile.VERTICAL)
            return
            
        (current_loc, direction) = self.get_location(border)
        # Alteractions where border currently matches in direction
        # (current_loc, wanted_loc)
        _alterations = {
            (Tile.LEFT, Tile.TOP): lambda x: x._rotate(Tile.CLOCKWISE, 90)._flip(Tile.VERTICAL),
            (Tile.LEFT, Tile.RIGHT): lambda x: x._flip(Tile.VERTICAL),
            (Tile.LEFT, Tile.BOTTOM): lambda x: x._rotate(Tile.ANTICLOCKWISE, 90),
            (Tile.TOP, Tile.RIGHT): lambda x: x._rotate(Tile.CLOCKWISE, 90),
            (Tile.TOP, Tile.BOTTOM): lambda x: x._flip(Tile.HORIZONTAL),
            (Tile.TOP, Tile.LEFT): lambda x: (x._flip(Tile.HORIZONTAL)._rotate(Tile.CLOCKWISE, 90)),
            (Tile.RIGHT, Tile.BOTTOM): lambda x: x._rotate(Tile.CLOCKWISE, 90)._flip(Tile.VERTICAL),
            (Tile.RIGHT, Tile.LEFT): lambda x: x._flip(Tile.VERTICAL), 
            (Tile.RIGHT, Tile.TOP): lambda x: x._rotate(Tile.ANTICLOCKWISE, 90),
            (Tile.BOTTOM, Tile.LEFT): lambda x: x._rotate(Tile.CLOCKWISE, 90),
            (Tile.BOTTOM, Tile.TOP): lambda x: x._flip(Tile.HORIZONTAL),
            (Tile.BOTTOM, Tile.RIGHT): lambda x: x._rotate(Tile.ANTICLOCKWISE, 90)._flip(Tile.HORIZONTAL)
            }
        
        _alterations[(current_loc, desired_loc)](self)
        if direction == Tile.OPPOSITE_DIRECTION:
            # Flip to make direction match
            if desired_loc in [Tile.TOP, Tile.BOTTOM]:
                self._flip(Tile.VERTICAL)
            else:
                self._flip(Tile.HORIZONTAL)
            

    def num_neighbours(self):
        n = len([x for x in self.unordered_neighbours if x is not None])
        if n == 0:
            raise RuntimeError(f"No neighbours set yet for id {self.id}")
        return n
    
    def add_neighbour(self, _id):
        if _id not in self.unordered_neighbours:
            self.unordered_neighbours.append(_id)
    
    def set_neighbour_position(self, _id, location):
        if not _id in self.unordered_neighbours:
            raise RuntimeError("No such neighbour")
        self.ordered_neighbours[location] = _id
    
    def set_position(self, x, y):
        self.position = (x, y)
        
    def get_position(self):
        return self.position
    
    def __str__(self):
        ret = ""
        for line in self.tile:
            ret += ("".join(line) + "\n")
        return ret
        

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

def get_neighbour(tile, tile_dict, location):
    # Get neighbour with tile matching right
    right_border = tile.borders[location]
    for n in tile.unordered_neighbours:
        if tile_dict[n].matches_any_border(right_border):
            return n
    return None

def create_row(tile_dict, left, row_no):
    """
    left-hand one must be correctly oriented
    """
    col_no = 0
    while True:
        # Get neighbour with border matching right
        left.set_position(row_no, col_no)
        right_id = get_neighbour(left, tile_dict, Tile.RIGHT)
        if right_id is None: return
        right_neighbour = tile_dict[right_id]
        right_neighbour.set_border(left.borders[Tile.RIGHT], Tile.LEFT)
        right_neighbour.neighbours[Tile.LEFT] = left.id
        left.neighbours[Tile.RIGHT] = right_neighbour.id
        left = right_neighbour
        col_no += 1
        
        
def order_tiles(tile_dict):
    topleft = get_corners(tile_dict)[0]
    topleft_id = topleft.id
    # Rotate/flip so that matched borders on right and bottom
    topleft.neighbours[topleft.RIGHT] = topleft.unordered_neighbours[0]
    for b in topleft.borders:
        if tile_dict[topleft.neighbours[Tile.RIGHT]].matches_any_border(b):
            topleft.set_border(b, Tile.RIGHT)
            
    topleft.neighbours[Tile.BOTTOM] = topleft.unordered_neighbours[1]
    for b in topleft.borders:
        if tile_dict[topleft.neighbours[Tile.BOTTOM]].matches_any_border(b):
            topleft.set_border(b, Tile.BOTTOM)
    
    row_no = 0
    while True:
        create_row(tile_dict, topleft, row_no)
        below_neighbour_id = get_neighbour(topleft, tile_dict, Tile.BOTTOM)
        if below_neighbour_id is None: break
        below_neighbour = tile_dict[below_neighbour_id]
        below_neighbour.set_border(topleft.borders[Tile.BOTTOM], Tile.TOP)
        below_neighbour.neighbours[Tile.TOP] = topleft.id
        topleft.neighbours[Tile.BOTTOM] = below_neighbour.id
        topleft = below_neighbour
        row_no += 1
        
    return topleft_id

def create_picture(tile_dict, topleft_id):
    
    tile_width = tile_dict[topleft_id].tile.shape[0] - 2
    tile_height = tile_dict[topleft_id].tile.shape[1] - 2
    
    def _get_size():
        def _get_horizontal():
            _id = topleft_id
            horizontal = 1
            while tile_dict[_id].neighbours[Tile.RIGHT] is not None:
                horizontal += 1
                _id = tile_dict[_id].neighbours[Tile.RIGHT]
            return horizontal
        def _get_vertical():
            _id = topleft_id
            vertical = 1
            while tile_dict[_id].neighbours[Tile.BOTTOM] is not None:
                vertical += 1
                _id = tile_dict[_id].neighbours[Tile.BOTTOM]
            return vertical
        return (_get_horizontal() * tile_width,
                _get_vertical() * tile_height)
    full_pic = np.empty(_get_size(), dtype=tile_dict[topleft_id].tile.dtype)
    
    for tile in tile_dict.values():
        left_corner = tile.get_position()[0] * tile_width
        right_corner = tile.get_position()[1] * tile_height
        full_pic[left_corner:left_corner+tile_width,
                  right_corner:right_corner+tile_height] = tile.tile[1:-1, 1:-1]
    
    return full_pic

def number_sea_monsters(picture):
    sea_monster = np.array([list("                  # "),
                            list("#    ##    ##    ###"),
                            list(" #  #  #  #  #  #   ")])
    has_locations = []
    for i in range(len(sea_monster)):
        for j in range(len(sea_monster[0])):
            if sea_monster[i, j] == "#":
                has_locations.append((i, j))
                
    def has_monster_at(i, j):
        for (ix, jx) in has_locations:
            if picture[i+ix, j+jx] != "#": return False
        return True
    
    num_monsters = 0
    for i in range(len(picture) - len(sea_monster)):
        for j in range(len(picture[0]) - len(sea_monster[0])):
            if has_monster_at(i, j): num_monsters += 1
    return num_monsters

def run(input_type):
    tile_dict = get_input(input_type)
    for (_id, tile) in tile_dict.items():
        other_tiles = list(filter(lambda x: x[0] != _id, tile_dict.items()))
        for (other_id, other_tile) in other_tiles:
            if any(other_tile.matches_any_border(border) for border in tile.borders):
                tile.add_neighbour(other_id)
                other_tile.add_neighbour(_id)
    
    topleft_id = order_tiles(tile_dict)
    
    picture = create_picture(tile_dict, topleft_id)
    
    def _get_rot(picture):
        for k in range(4):
            n = number_sea_monsters(np.rot90(picture, k=k))
            if n != 0:
                return n
        for k in range(4):
            n = number_sea_monsters(np.fliplr(np.rot90(picture, k=k)))
            if n != 0:
                return n
        raise RuntimeError("Cannot find any monsters!")

    num_monsters = _get_rot(picture)
    print(f"n={num_monsters} monsters")
    
    HASHES_PER_MONSTER = 15
    num_hash_in_monsters = num_monsters * HASHES_PER_MONSTER

    num_hashes = (picture == "#").sum()

    print(f"Number of hashes left: {num_hashes - num_hash_in_monsters}")

def _p(picture):
    ret = ""
    for line in picture:
        ret += ("".join(line) + "\n")
    return ret
        