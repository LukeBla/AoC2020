'''
Created on 5 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(5)

import math


def get_partitioner(length, low_char, high_char):
    def get_row(char_str):
        if not length == ( 2 ** len(char_str)):
            raise RuntimeError(f"Expected character string of length {int(math.log2(length))}")
        row_low = 0
        row_high = length
        for c in char_str:
            if c == low_char:
                row_high = (row_low + row_high) // 2
            elif c == high_char:
                row_low = (row_low + row_high) // 2
            else:
                raise RuntimeError(f"Unexpected character {c} in {char_str} - expecting one of {low_char} or {high_char}")
        return row_high - 1
    return get_row

g8 = get_partitioner(8, "L", "R")
g128 = get_partitioner(128, "F", "B")

def get_location(char_str):
    row = g128(char_str[:7])
    col = g8(char_str[7:])
    seat_id = row * 8 + col
    return (row, col, seat_id)


with open("input.txt") as f:
    max_id = 0
    for line in f.readlines():
        line = line.rstrip()
        max_id = max(max_id, get_location(line)[2])

