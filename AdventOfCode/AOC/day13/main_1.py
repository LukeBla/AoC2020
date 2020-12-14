'''
Created on 13 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(13)

import numpy as np

def get_input(input_type):
    if input_type == "test":
        ret = {"earliest_t":939,
                "buses":"7,13,x,x,59,x,31,19".split(",")}
    else:
        ret = {}
        with open("input.txt") as f:
            ret["earliest_t"] = int(f.readline().strip())
            ret["buses"] = f.readline().strip().split(",")
    return ret


def run(input_type):
    _input = get_input(input_type)
    earliest_t = _input["earliest_t"]
    buses = np.array(sorted([int(bus_id) for bus_id in _input["buses"] if bus_id != "x"]))
    first_after_earliest = buses * np.ceil(earliest_t / buses).astype(int)
    min_index = first_after_earliest.argmin()
    bus_no = buses[min_index]
    bus_departure = first_after_earliest[min_index]
    wait = bus_departure - earliest_t
    print(f"Bus {bus_no} departing as {bus_departure} wait {wait} - product = {bus_no * wait}")
    

