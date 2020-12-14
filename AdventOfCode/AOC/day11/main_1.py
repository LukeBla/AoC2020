'''
Created on 11 Dec 2020

@author: Luke
'''
from AOC.config import config
config.set_wd(11)

import numpy as np

def get_input(input_type):
    if input_type == "test":
        lst = ["L.LL.LL.LL",
        "LLLLLLL.LL",
        "L.L.L..L..",
        "LLLL.LL.LL",
        "L.LL.LL.LL",
        "L.LLLLL.LL",
        "..L.L.....",
        "LLLLLLLLLL",
        "L.LLLLLL.L",
        "L.LLLLL.LL"]
    else:
        with open("input.txt") as f:
            lst = f.readlines()
    
    return np.array(list(map(lambda x: [c for c in x.strip()], lst)))


def update_time(current_layout):
    """
    Get the layout after time is updated
    """
    
    def is_seat(i, j):
        return current_layout[i, j] in ("L", "#")
    
    def get_square_around(i, j):
        (imax, jmax) = current_layout.shape
        return current_layout[max(i-1, 0):min(i+2, imax), max(j-1, 0):min(j+2, jmax)]
    
    def num_occupied_around(i, j):
        """
        Get number of seats occupied around
        the seat at (i, j).
        Get total number of occupied seats in square including
        (i,j) then remove 1 if (i,j) was occupied
        """
        total_occupied = np.sum((get_square_around(i,j) == "#"))
        if current_layout[i,j] == "#":
            return total_occupied - 1
        else:
            return total_occupied
    
    ret = np.copy(current_layout)
    (imax, jmax) = current_layout.shape
    for i in range(imax):
        for j in range(jmax):
            if not is_seat(i, j): continue
            occupied_around = num_occupied_around(i, j)
            if current_layout[i, j] =="L" and occupied_around == 0:
                ret[i, j] = "#"
            elif current_layout[i, j] == "#" and occupied_around >= 4:
                ret[i, j] = "L"
    return ret

def run(input_type):
    input = get_input(input_type)
    while True:
        new_input = update_time(input)
        if np.all(input == new_input):
            occupied_seats = np.sum(input == "#")
            print(f"Reached steady state - {occupied_seats} occupied seats")
            return
        input = new_input

