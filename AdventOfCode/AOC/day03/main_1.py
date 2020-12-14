'''
Created on 4 Dec 2020

@author: Luke
'''

X_INCREMENT = 3

from AOC.config import config
config.set_wd(3)

def process_line(x_coord, trees_encountered, line):
    if line[x_coord-1] == "#":
        trees_encountered += 1
    x_coord += X_INCREMENT
    if x_coord > len(line):
        x_coord = x_coord % len(line)
    return (x_coord, trees_encountered)


x_coord = 1
trees_encountered = 0
with open("input.txt") as f:
    for line in f.readlines():
        (x_coord, trees_encountered) = process_line(x_coord, trees_encountered, line.rstrip())
    
print(f"Encountered {trees_encountered} trees")