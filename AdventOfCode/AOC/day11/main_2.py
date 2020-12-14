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
    
    def num_occupied_around(i, j):
        
        def first_seat_occupied_in_direction(delta_i, delta_j):
            """
            delta_i, delta_j 0s, 1s or -1s giving direction to look in
            """
            (imax, jmax) = current_layout.shape
            factor = 1
            while True:
                itest = i + (factor * delta_i)
                jtest = j + (factor * delta_j)
                if itest < 0 or itest >= imax or jtest < 0 or jtest >= jmax:
                    return False
                elif current_layout[itest, jtest] == "#":
                    return True
                elif current_layout[itest, jtest] == "L":
                    return False
                factor += 1
        occupied_seats = 0
        for delta_i in [-1, 0, 1]:
            for delta_j in [-1, 0, 1]:
                if (delta_i, delta_j) == (0, 0): continue
                if first_seat_occupied_in_direction(delta_i, delta_j): occupied_seats += 1
        return occupied_seats

    ret = np.copy(current_layout)
    (imax, jmax) = current_layout.shape
    for i in range(imax):
        for j in range(jmax):
            if not is_seat(i, j): continue
            occupied_around = num_occupied_around(i, j)
            if current_layout[i, j] =="L" and occupied_around == 0:
                ret[i, j] = "#"
            elif current_layout[i, j] == "#" and occupied_around >= 5:
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

