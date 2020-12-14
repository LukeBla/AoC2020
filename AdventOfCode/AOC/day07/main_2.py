'''
Created on 7 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(7)

import re

bag_list = {}

class Bag(object):
    
    def __init__(self, description):
        global bag_list
        self.description = description
        self.parse_description()
        if self.colour in bag_list:
            raise RuntimeError(f"{self.colour} already in list")
        bag_list[self.colour] = self
        self.parents = []
        self.ancestors = []
    
    def parse_description(self):
        regex = r'([a-z]+ [a-z]+) bags contain (.*)\.'
        match = re.match(regex, self.description)
        if match is None:
            raise RuntimeError(f"Cannot parse description {self.description}")
        self.colour = match.group(1)
        contents = match.group(2)
        self.children = []
        if contents == "no other bags":
            return
        for child in map(str.strip, contents.split(",")):
            regex = r'([0-9]+) ([a-z]+ [a-z]+) bags?'
            match = re.match(regex, child)
            if match is None:
                raise RuntimeError(f"Cannot parse child {child}")
            self.children.append((match.group(2), match.group(1)))
    
    def get_num_bags(self):
        num_bags = 1
        for (name, num) in self.children:
            num = int(num)
            num_bags += (num * bag_list[name].get_num_bags())
        return num_bags
    
    def __str__(self):
        children = ", ".join([f"{col}: {num}" for (col, num) in self.children])
        return f"[{self.colour}] - {children}"


def read_input():
    global bag_list
    with open("input.txt") as f:
        for line in f.readlines():
            b = Bag(line)

def read_example():
    global bag_list
    example = [
    "shiny gold bags contain 2 dark red bags.",
    "dark red bags contain 2 dark orange bags.",
    "dark orange bags contain 2 dark yellow bags.",
    "dark yellow bags contain 2 dark green bags.",
    "dark green bags contain 2 dark blue bags.",
    "dark blue bags contain 2 dark violet bags.",
    "dark violet bags contain no other bags."
    ]
    for line in example:
        b = Bag(line)

read_input()
our_bag = "shiny gold"
print(f"{our_bag}: must altogether have {bag_list[our_bag].get_num_bags()-1} bags")

    