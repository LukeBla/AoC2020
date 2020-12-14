'''
Created on 8 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(8)

import copy

class Boot(object):
    def __init__(self):
        self.accumulator = 0
        self.index = 0
        self.original_instructions = []
        self.instructions = []
        self.run_indexes = []
        
    def parse_instructions(self, instructions):
        for i in instructions:
            (op, arg) = map(str.strip, i.split())
            arg = int(arg)
            self.original_instructions.append((op, arg))
        self.instructions = copy.copy(self.original_instructions)
    
    def can_switch_instruction(self, index):
        return self.original_instructions[index][0] in ("nop", "jmp")
    
    def switch_instruction(self, index):
        """
        Swap a nop to a jmp, or vica versa, at the given
        index
        """
        self.reset()
        (op, arg) = self.original_instructions[index]
        if op == "nop":
            self.instructions[index] = ("jmp", arg)
        elif op == "jmp":
            self.instructions[index] = ("nop", arg)
        else:
            raise RuntimeError("Can only switch jmp/nop instructions")
        
    def reset(self):
        self.accumulator = 0
        self.index = 0
        self.instructions = copy.copy(self.original_instructions)
        self.run_indexes = []
            
    def completes(self):
        while self.index not in self.run_indexes:
            self.run_indexes.append(self.index)
            try:
                (op, arg) = self.instructions[self.index]
            except IndexError:
                return True
            if op == "nop":
                self.index += 1
            elif op == "acc":
                self.accumulator += arg
                self.index += 1
            elif op == "jmp":
                self.index += arg
            else:
                raise RuntimeError(f"Unexpected operations {op}")
        return False
        
b = Boot()
with open("input.txt") as f:
    b.parse_instructions(f.readlines())
for i in range(len(b.original_instructions)):
    if b.can_switch_instruction(i):
        b.switch_instruction(i)
        if b.completes():
            print(f"Instruction {i} switch completed - accumulator = {b.accumulator}")
            break
                