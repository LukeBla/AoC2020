'''
Created on 17 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(17)

import numpy as np

def get_input(input_type):
    if input_type == "test":
        arr =[[".","#","."],
             [".",".","#"],
             ["#","#","#"]]
    else:
        arr = []
        with open("input.txt") as f:
            for line in f:
                arr.append(list(line.strip()))
    return np.array(arr, dtype="S1")


class ConwayCube(object):
    # Need to use byte form as numpy turns S1 into byte array and can only do element-wise
    # comparisons if comparing with byte object
    active = b"#"
    inactive = b"."
    def __init__(self, initial_state):
        self.side_len = len(initial_state)
        self.cube = np.full((self.side_len, self.side_len, self.side_len, self.side_len), self.inactive, dtype="S1")
        self.cube[1,1] = initial_state
        
    def num_active_around(self, i, j, k, w):
        """
        Number of active sites around the point (i, j)
        """
        surrounding_cube = self.cube[max(0, i-1):i+2,
                                     max(0, j-1):j+2,
                                     max(0, k-1):k+2,
                                     max(0, w-1):w+2]
        active_around = (surrounding_cube == self.active).sum()
        if self.cube[i, j, k, w] == self.active:
            return active_around - 1
        else:
            return active_around
        
    def next_state(self, i, j, k, w):
        if self.cube[i, j, k, w] == self.active:
            if self.num_active_around(i, j, k, w) in [2,3]:
                return self.active
            else:
                return self.inactive
        else:
            if self.num_active_around(i, j, k, w) == 3:
                return self.active
            else:
                return self.inactive
        
    def step(self):
        self.side_len += 2
        # Extend cube by +1 in each direction
        embedded_cube = np.full((self.side_len, self.side_len, self.side_len, self.side_len), self.inactive, dtype="S1")
        embedded_cube[1:self.side_len-1, 1:self.side_len-1, 1:self.side_len-1, 1:self.side_len-1] = self.cube
        self.cube = embedded_cube
        next_cube = embedded_cube.copy()
        for i in range(self.side_len):
            for j in range(self.side_len):
                for k in range(self.side_len):
                    for w in range(self.side_len):
                        next_cube[i, j, k, w] = self.next_state(i, j, k, w)
        self.cube = next_cube

    def num_active_cubes(self):
        return (self.cube == self.active).sum()
    
    def __str__(self):
        def _get_str_slice(i):
            ret = ""
            for j in range(self.side_len):
                ret += "\n" + "".join(map(lambda x: x.decode("utf-8"), self.cube[i, j]))
            return ret
        ret = ""
        z_offset = self.side_len // 2
        for i in range(self.side_len):
            ret += f"z={i-z_offset}{_get_str_slice(i)}\n\n"
        return ret
        
        
def run(input_type):
    c = ConwayCube(get_input(input_type))
    for i in range(6):
        c.step()
    print(f"After 6 steps - {c.num_active_cubes()} cubes")
        
        