'''
Created on 4 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(2)

import re

def parse_str(input_str):
    match_re = r'(\d+)-(\d+) ([a-z]): ([a-z]+)'
    m = re.match(match_re, input_str)
    if m is None:
        raise RuntimeError(f"No match for string '{input_str}'")
    return m.groups()


def valid_password(char, nmin, nmax, pwd):
    num_char_in_str = len([ x for x in pwd if x == char])
    return nmin <= num_char_in_str <= nmax
    
def valid_line(line):
    (nmin, nmax, char, pwd) = parse_str(line)
    nmin = int(nmin)
    nmax = int(nmax)
    return valid_password(char, nmin, nmax, pwd)

num_valid = 0
with open("input.txt") as f:
    for line in f.readlines():
        if valid_line(line.rstrip()):
            num_valid += 1
        
print(f"{num_valid} valid passwords")