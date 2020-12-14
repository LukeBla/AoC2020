'''
Created on 4 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(4)

import re

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

def get_field(keyval):
    regex = r"([a-z]{3}):.*"
    m = re.match(regex, keyval)
    if m is None:
        raise RuntimeError(f"No match for {keyval}")
    return m.groups()[0]

def valid_passport(passport):
    return set(required_fields) <= set([get_field(x) for x in passport.split(" ") if x != ""])

passport=""
valid_passports = 0
with open("input.txt") as f:
    for line in f.readlines():
        line = line.rstrip()
        if line == "":
            if passport:
                valid_passports += int(valid_passport(passport))
                passport = ""
        else:
            passport += (" " + line)
        