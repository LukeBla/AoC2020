'''
Created on 9 Dec 2020

@author: Luke
'''



from AOC.config import config
config.set_wd(9)
import itertools
import numpy as np


class NumberChecker(object):
    
    def __init__(self, input_filename, N):
        self.N = N
        self.file_obj = open(input_filename)
        self.data = []
        self.all_data = []
        for _ in range(N):
            next_val = int(self.file_obj.readline().strip())
            self.data.append(next_val)
            self.all_data.append(next_val)
    
    def find_weakness(self):
        """
        Find contiguous sum in all data that sums to invalid number.
        Return sum of smallest and largest value
        """
        for start in itertools.count(start=0):
            for length in itertools.count(start=2):
                subset = self.all_data[start:start+length]
                subset_sum = np.sum(subset, dtype="int64")
                if subset_sum == self.first_invalid:
                    # We've found it
                    return np.min(subset) + np.max(subset)
                elif subset_sum > self.first_invalid:
                    break
            
    
    def next_line_valid(self):
        next_num = int(self.file_obj.readline().strip())
        all_sums = set([self.data[i] + self.data[j] for i in range(len(self.data)) for j in range(len(self.data)) if i != j])
        if next_num not in all_sums:
            self.first_invalid = next_num
            return False
        self.data.pop(0)
        self.data.append(next_num)
        self.all_data.append(next_num)
        return True
            
    def __del__(self):
        self.file_obj.close()


n = NumberChecker("input.txt", 25)
while n.next_line_valid():
    pass
print(f"First invalid number: {n.first_invalid}")
print(f"Weakness is: {n.find_weakness()}")
del n

