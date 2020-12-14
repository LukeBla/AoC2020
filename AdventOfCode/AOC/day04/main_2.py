'''
Created on 4 Dec 2020

@author: Luke
'''
'''
Created on 4 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(4)

import re

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

def get_field(keyval):
    regex = r"([a-z]{3}):(.*)"
    m = re.match(regex, keyval)
    if m is None:
        raise RuntimeError(f"No match for {keyval}")
    return list(map(str.strip, m.groups()))

def validate(key, val):
    if key in ["byr", "iyr", "eyr"]:
        lims = {"byr":[1920, 2002], "iyr":[2010,2020], "eyr":[2020,2030]}
        if re.match(r"^[0-9]{4}$", val) is None:
            return False
        val = int(val)
        return lims[key][0] <= val <= lims[key][1]
    elif key == "hgt":
        ret = re.match("([0-9]+)(cm|in)", val)
        if ret is None: return False
        (num, unit) = ret.groups()
        if unit == "cm":
            return 150 <= int(num) <= 193
        else:
            return 59 <= int(num) <= 76
    elif key == "hcl":
        return re.match("^#[0-9a-f]{6}$", val) is not None
    elif key == "ecl":
        return val in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    elif key == "pid":
        return re.match("^[0-9]{9}$", val) is not None
    else:
        return False


def valid_passport(passport):
    required = {"byr":False, "iyr":False, "eyr":False,
                "hgt":False, "hcl":False, "ecl": False, "pid":False}
    for keyval in [ x for x in map(str.strip, passport.split(" ")) if x != ""]:
        (key, val) = get_field(keyval)
        if key == "cid": continue
        required[key] = validate(key, val)
    return all(required.values())


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
