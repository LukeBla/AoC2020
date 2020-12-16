'''
Created on 15 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(15)


def get_input(input_type):
    if input_type == "test1":
        return [0, 3, 6]
    elif input_type == "test2":
        return [1, 3, 2]
    elif input_type == "test3":
        return [2, 1, 3]
    elif input_type == "test4":
        return [1, 2, 3]
    elif input_type == "test5":
        return [2, 3, 1]
    elif input_type == "test6":
        return [3, 2, 1]
    elif input_type == "test7":
        return [3, 1, 2]
    else:
        return [9, 3, 1, 0, 8, 4]
    
class MemoryGame(object):
    def __init__(self, starting_nums):
        self.last_mentioned_on = {}
        for (i, no) in enumerate(starting_nums[:-1]):
            self.last_mentioned_on[no] = i+1
            
        # Initialise first round
        self.prev_no = starting_nums[-1]
        self.prev_round = len(starting_nums)
        self.numbers = starting_nums[:-1]

    
    def next(self):
        self.numbers.append(self.prev_no)
        if self.prev_no in self.last_mentioned_on:
            dist = self.prev_round - self.last_mentioned_on[self.prev_no]
            self.last_mentioned_on[self.prev_no] = self.prev_round
            self.prev_no = dist
        else:
            self.last_mentioned_on[self.prev_no] = self.prev_round
            self.prev_no = 0

        self.prev_round += 1
        return self.prev_no
    
def run(input_type):
    _input = get_input(input_type)
    m = MemoryGame(_input)
    for _ in range(2020-len(_input)): # Take account of initial rounds
        ret = m.next()
    print(ret)
        
        