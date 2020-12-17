'''
Created on 16 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(16)

import re
import numpy as np

def get_input(input_type):
    if input_type == "test":
        ret = {"rules":["class: 0-1 or 4-19", "row: 0-5 or 8-19", "seat: 0-13 or 16-19"],
                "your_ticket":[11,12,13],
                "other_tickets":[[3,9,18], [15,1,5], [5,14,9]]}
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
        self.rule_order = {}
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
    
    def all_match_rule(self, name, values):
        """
        Whether every one of the given values matches the rule
        """
        return all([self.matches_rule(name, value) for value in values])
    
    def get_matching_rule(self, values, ignore_rules=[]):
        """
        Return the rule that matches all the given values, ignoring already known rules.
        Check there is only one rule that does so - if there are many then
        return None
        """
        ordered_rules = np.array([r for r in self.rules.keys() if r not in ignore_rules])
        matches_values = np.array([self.all_match_rule(rule, values) for rule in ordered_rules])
        if sum(matches_values) == 0:
            raise RuntimeError(f"No rules found to match values '{values}'")
        elif sum(matches_values) > 1:
            return None
        else:
            return ordered_rules[matches_values][0]
    
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
    # Get only valid tickets
    other_tickets = list(filter(lambda t: t.is_valid(), [Ticket(v, rules) for v in _input["other_tickets"]]))
    rule_order = [None for i in range(len(other_tickets[0].values))]
    while len([x for x in rule_order if x is None]) > 0:
        for i in range(len(other_tickets[0].values)):
            if rule_order[i] is not None: continue
            rule_order[i] = rules.get_matching_rule([t.values[i] for t in other_tickets],
                                                      ignore_rules=[r for r in rule_order if r is not None])
    
    # Get indexes of rules that start with "d"
    start_with_d = np.array(list(map(lambda x: x.startswith("departure"), rule_order)))
    d_prod = np.prod(np.array(_input["your_ticket"], dtype="int64")[start_with_d])
    print(f"Product is {d_prod}")
        
    
    
    
            