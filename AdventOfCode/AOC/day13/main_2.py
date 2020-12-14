'''
Created on 13 Dec 2020

@author: Luke
'''

'''
Created on 13 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(13)

import numpy as np

def get_input(input_type):
    if input_type == "test1":
        ret = {"earliest_t":939,
                "buses":"7,13,x,x,59,x,31,19".split(",")}
    elif input_type == "test2":
        ret = {"earliest_t":None,
               "buses":"17,x,13,19".split(",")}
    elif input_type == "test3":
        ret = {"earliest_t":None,
               "buses":"67,7,59,61".split(",")}
    elif input_type == "test4":
        ret = {"earliest_t":None,
               "buses":"67,x,7,59,61".split(",")}
    elif input_type == "test5":
        ret = {"earliest_t":None,
               "buses":"67,7,x,59,61".split(",")}
    elif input_type == "test6":
        ret = {"earliest_t":None,
               "buses":"1789,37,47,1889".split(",")}
    else:
        ret = {}
        with open("input.txt") as f:
            ret["earliest_t"] = int(f.readline().strip())
            ret["buses"] = f.readline().strip().split(",")
    return ret

def run(input_type):
    from functools import reduce
    # Chinese remainder theorem taken from https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
    def chinese_remainder(n, a):
        sum = 0
        prod = reduce(lambda a, b: a*b, n)
        for n_i, a_i in zip(n, a):
            p = prod // n_i
            sum += a_i * mul_inv(p, n_i) * p
        return sum % prod
     
     
     
    def mul_inv(a, b):
        b0 = b
        x0, x1 = 0, 1
        if b == 1: return 1
        while a > 1:
            q = a // b
            a, b = b, a%b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0: x1 += b0
        return x1
     
    n = get_input(input_type)["buses"]
    a = np.array([x for x in range(len(n)) if n[x] != "x"], dtype="int64")
    n = np.array([ int(n[i]) for i in a], dtype="int64")
    a = n - a
    print(chinese_remainder(n, a))