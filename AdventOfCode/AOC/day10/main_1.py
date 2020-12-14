'''
Created on 10 Dec 2020

@author: Luke
'''



from AOC.config import config
config.set_wd(10)

test_input_1 = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]

test_input_2 = [28, 33, 18, 42, 31, 14, 46, 20, 48,
47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35,
8, 17, 7, 9, 4, 2, 34, 10, 3]

def run(input):
    input = sorted(input)
    diffs = []
    for i in range(len(input)-1):
        diffs.append(input[i+1] - input[i])
    diff_nos = {}
    for i in set(diffs):
        diff_nos[i] = len([d for d in diffs if d == i])
    # Add initial diff (smallest values) and finall diff (3)
    diff_nos[min(input)] += 1
    diff_nos[3] += 1
    return diff_nos

with open("input.txt") as f:
    input = map(lambda x: int(x.strip()), f.readlines())
ret = run(input)
print(f"Jolts: {ret} - prod is {ret[1] * ret[3]}")