'''
Created on 14 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(14)

import re


class Memory(object):
    def __init__(self):
        self.bitmask = None
        self.memory = {}
        
    def set_bitmask(self, bitmask):
        self.bitmask = list(bitmask)
        
    def set_memory(self, address, value):
        self.memory[address] = self.mask_value(value)
    
    def int_to_list(self, value):
        """
        Create 36-bit list of 0s and 1s
        """
        ret = []
        q = value
        for i in range(36):
            (q, r) = divmod(q, 2)
            ret = [r] + ret
        return ret
    
    def list_to_int(self, list_value):
        ret = 0
        mult = 1
        for i in range(35, -1, -1):
            ret += mult * list_value[i]
            mult *= 2
        return ret
    
    def mask_value(self, value):
        list_value = self.int_to_list(value)
        ret = [None for i in range(36)]
        for i in range(36):
            if self.bitmask[i] == "X":
                ret[i] = list_value[i]
            else:
                ret[i] = int(self.bitmask[i])
        return self.list_to_int(ret)
    
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
        ret = ["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
                "mem[8] = 11", "mem[7] = 101", "mem[8] = 0"]
    else:
        with open("input.txt") as f:
            ret = map(str.strip, f.readlines())
    return ret

def run(input_type):
    m = Memory()
    for line in get_input(input_type):
        m.parse(line)
    print(m.get_sum())

