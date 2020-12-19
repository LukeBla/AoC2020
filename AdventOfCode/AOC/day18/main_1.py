'''
Created on 18 Dec 2020

@author: Luke
'''
import re

from AOC.config import config
config.set_wd(18)

import operator

def get_input(input_type):
    if input_type == "test1":
        return ["1 + 2 * 3 + 4 * 5 + 6"]
    elif input_type == "test2":
        return ["1 + (2 * 3) + (4 * (5 + 6))"]
    elif input_type == "test3":
        return ["2 * 3 + (4 * 5)"]
    elif input_type == "test4":
        return ["5 + (8 * 3 + 9 + 3 * 4 * 3)"]
    elif input_type == "test5":
        return ["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]
    elif input_type == "test6":
        return ["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]
    else:
        with open("input.txt") as f:
            return list(map(str.strip, f.readlines()))

def lexical_split(input_str):
    ret = []
    numerical = ""
    paren_level=0
    for c in input_str:
        m =  re.match("[0-9]", c)
        if m is not None:
            numerical += c
        else:
            if numerical != "":
                ret.append(int(numerical))
                numerical = ""
            if c == " ":
                continue
            elif c == "(":
                paren_level += 1
                ret.append(f"OPAREN_{paren_level}")
            elif c == ")":
                ret.append(f"CPAREN_{paren_level}")
                paren_level -= 1
            else:
                ret.append(c)
    if numerical != "":
        ret.append(int(numerical))
    return ret

def unflatten_list(input_list):
    """
    Convert sub-expressions into sublists
    """
    i = 0
    ret = []
    while i < len(input_list):
        if type(input_list[i]) == str and input_list[i].startswith("OPAREN"):
            paren_level = input_list[i].replace("OPAREN_","")
            cparen_i = i + input_list[i:].index(f"CPAREN_{paren_level}")
            ret.append(unflatten_list(input_list[i+1:cparen_i]))
            i = cparen_i + 1
        else:
            ret.append(input_list[i])
            i += 1
    return ret
    
class ExpressionTree(object):
    def __init__(self, left, op, right):
        while isinstance(left, list) and len(left) == 1:
            left = left[0]
        while isinstance(right, list) and len(right) == 1:
            right = right[0]
        if isinstance(left, list):
            left = ExpressionTree(left[:-2], left[-2], left[-1])
        if isinstance(right, list):
            right = ExpressionTree(right[:-2], right[-2], right[-1])
        self.left = left
        self.right = right
        self.op = op
        
    def eval(self):
        if isinstance(self.left, ExpressionTree):
            left = self.left.eval()
        else:
            left = self.left
        if isinstance(self.right, ExpressionTree):
            right = self.right.eval()
        else:
            right = self.right
        op_map = {"+":operator.add, "-":operator.sub, "*":operator.mul}
        return op_map[self.op](left, right)
        
    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

def get_tree(multi_list):
    return ExpressionTree(multi_list[:-2], multi_list[-2], multi_list[-1])

def run(input_type):
    ret = []
    for _input in get_input(input_type):
        multi_list = unflatten_list(lexical_split(_input))
        tree = get_tree(multi_list)
        ret.append(tree.eval())
    print(f"Sum = {sum(ret)}")
        
    