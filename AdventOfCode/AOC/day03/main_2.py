'''
Created on 4 Dec 2020

@author: Luke
'''

'''
Created on 4 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(3)


def run(x_increment, y_increment):
    def process_line(x_coord, trees_encountered, line):
        if line[x_coord-1] == "#":
            trees_encountered += 1
        x_coord += x_increment
        if x_coord > len(line):
            x_coord = x_coord % len(line)
        return (x_coord, trees_encountered)
    
    
    x_coord = 1
    trees_encountered = 0
    lineno = 0
    with open("input.txt") as f:
        for line in f.readlines():
            if (lineno % y_increment) == 0:
                (x_coord, trees_encountered) = process_line(x_coord, trees_encountered, line.rstrip())
            lineno += 1
    return trees_encountered

incs = [[1,1], [3, 1], [5,1], [7,1], [1,2]]
res_arr = []
for (x_inc, y_inc) in incs:
    res = run(x_inc, y_inc)
    res_arr.append(res)
    print(f"({x_inc}, {y_inc}): Encountered {res} trees")

import numpy as np
print(f"Product is {np.prod(res_arr, dtype='int64')}")