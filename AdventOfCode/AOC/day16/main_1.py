'''
Created on 16 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(16)

import re
import itertools

def get_input(input_type):
    if input_type == "test":
        ret = {"rules":["class: 1-3 or 5-7", "row: 6-11 or 33-44", "seat: 13-40 or 45-50"],
                "your_ticket":[7, 1, 14],
                "other_tickets":[[7,3,47], [40,4,50], [55,2,20], [38,6,12]]}
    else:
        def get_rules(fh):
            rules = []
            for line in fh:
                if line.strip() == "": return rules
                rules.append(line.strip())
        def get_your_ticket(fh):
            header = next(fh).strip()
            if header != "your ticket:":
                raise RuntimeError(f"Unexpected header '{header}' - expected 'your ticket:'")
            line = next(fh).strip()
            # Eat blank line
            next(fh)
            return list(map(int, line.split(",")))
        def get_other_tickets(fh):
            header = next(fh).strip()
            if header != "nearby tickets:":
                raise RuntimeError(f"Unexpected header '{header}' - expected 'nearby tickets:'")
            ret = []
            for line in fh:
                ret.append(list(map(int, line.strip().split(","))))
            return ret
        
        ret = {}
        with open("input.txt") as f:
            ret["rules"] = get_rules(f)
            ret["your_ticket"] = get_your_ticket(f)
            ret["other_tickets"] = get_other_tickets(f)
            
    return ret


class Rules(object):
    def __init__(self, rules):
        self.rules = {}
        for rule in rules:
            m = re.match("([a-z ]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)", rule)
            if m is None:
                raise RuntimeError(f"Could not match rule '{rule}'")
            (name, min_1, max_1, min_2, max_2) = m.groups()
            self.rules[name] = [[int(min_1), int(max_1)], [int(min_2), int(max_2)]]
            
    def matches_rule(self, name, value):
        """
        Whether the value matches the given rule
        """
        return ((self.rules[name][0][0] <= value <= self.rules[name][0][1]) or 
                (self.rules[name][1][0] <= value <= self.rules[name][1][1]))
        
    def matches_any_rule(self, value):
        return any([self.matches_rule(name, value) for name in self.rules])

class Ticket(object):
    def __init__(self, values, rules):
        self.values = values
        self.invalid_values = []
        for v in self.values:
            if not rules.matches_any_rule(v):
                self.invalid_values.append(v)
    
    def is_valid(self):
        return len(self.invalid_values) == 0

def run(input_type):
    _input = get_input(input_type)
    rules = Rules(_input["rules"])
    other_tickets = [Ticket(v, rules) for v in _input["other_tickets"]]
    print("Sum of invalid values: {}".format(sum(itertools.chain(*[t.invalid_values for t in other_tickets]))))
    
    
            