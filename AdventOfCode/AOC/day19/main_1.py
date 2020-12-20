'''
Created on 19 Dec 2020

@author: Luke
'''

from AOC.config import config
config.set_wd(19)
import re

def get_input(input_type):
    if input_type == "test1":
        rules = ['0: 1 2',
                 '1: "a"',
                 '2: 1 3 | 3 1',
                 '3: "b"']
        messages = []
    elif input_type == "test2":
        rules = ['0: 4 1 5',
                '1: 2 3 | 3 2',
                '2: 4 4 | 5 5',
                '3: 4 5 | 5 4',
                '4: "a"',
                '5: "b"']
        messages = ["ababbb", "bababa", "abbbab", "aaabbb", "aaaabbb"]
    else:
        rules = []
        messages = []
        with open("input.txt") as f:
            for line in f:
                line = line.strip()
                if line == "": break
                rules.append(line)
            for line in f:
                messages.append(line.strip())
        
    return (rules, messages)



class Rule(object):
    def __init__(self, rule, rule_dict):
        self.parse_rule(rule)
        self.rule_dict = rule_dict
        self.saved_rules = None
        
    def parse_rule(self, rule_str):
        (id, rule) = list(map(str.strip, rule_str.split(":")))
        self.id = int(id)
        rules = list(map(str.split, map(str.strip, rule.split("|"))))
        def to_int(rule):
            ret = []
            for r in rule:
                if '"' in r:
                    ret.append(r.replace('"', ""))
                else:
                    ret.append(int(r))
            return ret
        self.rules = list(map(to_int, rules))
    
    def __str__(self):
        return f"{self.id}: {self.rules}"
    
    def _concat_rules(self, rules1, rules2):
        return [ a + b for a in rules1 for b in rules2]
    
    def _is_base_rule(self):
        return(len(self.rules) == 1 ) and (len(self.rules[0]) == 1) and isinstance(self.rules[0][0], str)
    
    def get_rule(self):
        if self.saved_rules is not None:
            return self.saved_rules
        if self._is_base_rule():
            self.saved_rules = self.rules[0]
            return self.rules[0]
        else:
            ret = []
            for ruleset in self.rules:
                combrule = [""]
                for i in ruleset:
                    combrule = self._concat_rules(combrule, self.rule_dict[i].get_rule())
                ret.extend(combrule)
            self.saved_rules = ret
            return ret

def run(input_type):
    rule_dict = {}
    (rules, messages) = get_input(input_type)
    for rule in rules:
        rule_obj = Rule(rule, rule_dict)
        rule_dict[rule_obj.id] = rule_obj
    rule_match = rule_dict[0].get_rule()
    num_matching = 0
    for message in messages:
        if message in rule_match:
            num_matching += 1
    print(f"{num_matching} messages match")
    return (rule_match, messages)
    
    