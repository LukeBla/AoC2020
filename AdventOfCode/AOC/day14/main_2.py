'''
Created on 14 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(14)

import re
import numpy as np


class Memory(object):
    def __init__(self):
        self.bitmask = None
        self.memory = {}
        
    def set_bitmask(self, bitmask):
        self.bitmask = list(bitmask)
        
    def set_memory(self, address, value):
        for a in self.get_addresses(address):
            self.memory[a] = value
    
    def int_to_list(self, value, bitlen=36):
        """
        Create 36-bit list of 0s and 1s
        """
        ret = []
        q = value
        for i in range(bitlen):
            (q, r) = divmod(q, 2)
            ret = [r] + ret
        return ret
    
    def list_to_int(self, list_value, bitlen=36):
        ret = 0
        mult = 1
        for i in range(bitlen-1, -1, -1):
            ret += mult * list_value[i]
            mult *= 2
        return ret
    
    def expand_address(self, address_list):
        num_x = len([x for x in address_list if x == "X"])
        ret = []
        address_list = np.array(address_list)
        where_x = (address_list == "X")
        for i in range(2 ** num_x):
            a = address_list.copy()
            a[where_x] = self.int_to_list(i, bitlen=num_x)
            ret.append(list(map(int, list(a))))
        return ret
        
    
    def get_addresses(self, address):
        """
        Get all addresses corresponding to the current bitmask
        """
        list_address = self.int_to_list(address)
        ret = [None for i in range(36)]
        for i in range(36):
            if self.bitmask[i] == "X":
                ret[i] = "X"
            elif self.bitmask[i] == "0":
                ret[i] = int(list_address[i])                
            elif self.bitmask[i] == "1":
                ret[i] = 1
        address_list = self.expand_address(ret)
        return [self.list_to_int(r) for r in address_list]
    
    def get_sum(self):
        """
        Get sum of values in memory
        """
        return sum(self.memory.values())
    
    def parse(self, _input):
        if _input.startswith("mask"):
            mask = _input.split(" =")[1].strip()
            self.set_bitmask(mask)
        else:
            m = re.match("mem\[([0-9]+)\] = ([0-9]+)", _input)
            if m is None:
                raise RuntimeError(f"Cannot match string {_input}")
            (address, value) = m.groups()
            self.set_memory(int(address), int(value))


def get_input(input_type):
    if input_type == "test":
        ret = ["mask = 000000000000000000000000000000X1001X",
                "mem[42] = 100",
                "mask = 00000000000000000000000000000000X0XX",
                "mem[26] = 1"]
    else:
        with open("input.txt") as f:
            ret = map(str.strip, f.readlines())
    return ret

def run(input_type):
    m = Memory()
    for line in get_input(input_type):
        m.parse(line)
    print(m.get_sum())

