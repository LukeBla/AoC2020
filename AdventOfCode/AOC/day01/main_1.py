'''
Created on 4 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(1)

with open("input.txt") as f:
    data = list(map(int, f.readlines()))


for i in data:
    for j in data:
        for k in data:
            if i + j + k == 2020:
                print(f"{i} * {j} * {k} = {i*j*k}")