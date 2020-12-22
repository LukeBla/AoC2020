'''
Created on 21 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(21)

import re

def get_input(input_type):
    if input_type == "test":
        ret = ["mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
                "trh fvjkl sbzzf mxmxvkd (contains dairy)",
                "sqjhc fvjkl (contains soy)",
                "sqjhc mxmxvkd sbzzf (contains fish)"]
    else:
        ret = []
        with open("input.txt") as f:
            for line in f:
                ret.append(line.strip())
    return ret

# For each allergen git a list of all foods that contain it
# Then intersection of foods are possible allergens
def get_allergen_foods(_input):
    allergen_d = {}
    all_ingredients = [] # Include multiplicity
    for line in _input:
        m = re.match(r"([^(]*) \(contains ([^)]*)\)", line)
        ingredients = set(m.groups()[0].split())
        all_ingredients.extend(ingredients)
        allergens = map(str.strip, m.groups()[1].split(", "))
        for allergen in allergens:
            if allergen not in allergen_d:
                allergen_d[allergen] = []
            allergen_d[allergen].append(ingredients)
    return (allergen_d, all_ingredients)

def get_possible_ingredients(ingredients):
    # Return intersection of all ingredients
    return set.intersection(*ingredients)

def get_nonallergens(possible_allergens, all_ingredients):
    return all_ingredients.difference(possible_allergens)

def run(input_type):
    _input = get_input(input_type)
    (allergen_d, all_ingredients) = get_allergen_foods(_input)
    
    reduced_allergen_d = {}
    for allergen in allergen_d:
        reduced_allergen_d[allergen] = get_possible_ingredients(allergen_d[allergen])
    # Get all ingredients that cannot have any allergens
    non_allergens = get_nonallergens(set.union(*list(reduced_allergen_d.values())), set(all_ingredients))
    
    # How many times to any of these appear in all the ingredient lists
    in_ingredients = [ x for x in all_ingredients if x in non_allergens]
    
    print(len(in_ingredients))