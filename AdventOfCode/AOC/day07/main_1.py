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
    
    def add_parent(self, parent):
        self.parents.append(parent)
    
    def get_ancestors(self):
        if not self.ancestors:
            self.ancestors = set(self.parents)
            for parent in self.parents:
                self.ancestors = self.ancestors.union(bag_list[parent].get_ancestors())
        return self.ancestors
    
    def __str__(self):
        children = ", ".join([f"{col}: {num}" for (col, num) in self.children])
        return f"[{self.colour}] - {children}"


def read_input():
    global bag_list
    with open("input.txt") as f:
        for line in f.readlines():
            b = Bag(line)

    
def create_tree():
    global bag_list
    for (colour, node) in bag_list.items():
        for child in node.children:
            bag_list[child[0]].add_parent(colour)
    
read_input()
create_tree()
our_bag = "shiny gold"
print(f"{our_bag}: can be contained in {len(set(bag_list[our_bag].get_ancestors()))}")

    