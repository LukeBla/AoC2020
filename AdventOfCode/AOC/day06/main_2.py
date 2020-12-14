'''
Created on 6 Dec 2020

@author: Luke
'''



from AOC.config import config
config.set_wd(6)

import numpy as np

def num_all_yes(group):
    s = set(group[0])
    for ns in group[1:]:
        s = s.intersection(ns)
    return len(s)

group_any_yes = []
with open("input.txt") as f:
    group = []
    for line in f.readlines():
        line = line.rstrip()
        if line == "":
            group_any_yes.append(num_all_yes(group))
            group = []
        else:
            group.append(line)
    # Need to add final group!
    group_any_yes.append(num_all_yes(group))
            
print(np.sum(group_any_yes, dtype="int64"))