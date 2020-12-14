'''
Created on 10 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(10)

def get_input(input_type="main"):
    if input_type == "test1":
        return [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]
    elif input_type == "test2":
        return [28, 33, 18, 42, 31, 14, 46, 20, 48,
                47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35,
                8, 17, 7, 9, 4, 2, 34, 10, 3]
    elif input_type == "main":
        with open("input.txt") as f:
            input = map(lambda x: int(x.strip()), f.readlines())
        return input
    
SOURCE_JOLTS = 0
DESTINATION_JOLTS = 22


import numpy as np

combinations_from = {}
def get_no_combinations(current_jolts, adapters):
    global combinations_from
    if current_jolts in combinations_from:
        return combinations_from[current_jolts]
    #print("---------------------------")
    #print(current_jolts)
    #print(adapters)
    if current_jolts == max(adapters):
        assert current_jolts >= DESTINATION_JOLTS - 3
        ret = 1
    else:
        no_combinations = {}
        for d in [1,2,3]:
            output_range = current_jolts + d
            if output_range in adapters:
                #print("*************************")
                no_combinations[d] = get_no_combinations(output_range, adapters[adapters.index(output_range):])
                #print("||||||||||||||||||||||||||")
        #print(no_combinations)
        ret = np.sum(list(no_combinations.values()), dtype="int64")
    combinations_from[current_jolts] = ret
    return ret

def run(input_type):
    return get_no_combinations(SOURCE_JOLTS, sorted(get_input(input_type)))
print(f"Number of combinations: {run('main')}")
    