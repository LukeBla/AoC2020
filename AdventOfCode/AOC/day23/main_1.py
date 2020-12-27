'''
Created on 23 Dec 2020

@author: Luke
'''


from AOC.config import config
config.set_wd(23)


class Cups(object):
    def __init__(self, cups):
        self.cups = cups
        self.current_cup = cups[0]
        self.picked_three = None
        self.destinaion = None
        
    def set_three(self):
        three = []
        #print(f"Picking three - cups = {self.cups}, current cup = {self.current_cup}")
        for _ in range(3):
            three.append(self.cups.pop((self.cups.index(self.current_cup)+1) % len(self.cups)))
        self.picked_three = three
        #print(f"Three = {self.picked_three}, cups = {self.cups}")
    
    def select_destination(self):
        #print("Selecting destination")
        dest = self.current_cup
        while True:
            dest -= 1
            if dest < min(self.cups): dest = max(self.picked_three + self.cups)
            if dest not in self.picked_three:
                self.destination = dest
                #print(f"Destination = {dest}")
                return
    
    def return_three(self):
        #print("Adding back three")
        dest_index = self.cups.index(self.destination)
        self.cups = self.cups[:dest_index+1] + self.picked_three + self.cups[dest_index+1:]
        #print(f"Cups = {self.cups}")
    
    def update_current(self):
        #print("Updating current cup")
        #print(f"Current cup was {self.current_cup}")
        if self.current_cup == self.cups[-1]:
            self.current_cup = self.cups[0]
        else:
            self.current_cup = self.cups[self.cups.index(self.current_cup) + 1]
        #print(f"Current cup is now {self.current_cup}")
    
    def get_final_num(self):
        # Concatenate numbers starting at value 1
        one_idx = self.cups.index(1)
        comb = self.cups[one_idx+1:] + self.cups[:one_idx]
        return "".join(map(str, comb))
    
    def run_round(self):
        self.picked_three = None
        self.destination = None
        self.set_three()
        self.select_destination()
        self.return_three()
        self.update_current()
            
        
def get_input(input_type):
    if input_type == "test":
        ret = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    else:
        ret = [9, 2, 5, 1, 7, 6, 8, 3, 4]
    return ret

def run(input_type):
    cups = Cups(get_input(input_type))
    for i in range(100):
        #print("=====================")
        #print(f"Move {i+1}")
        cups.run_round()
        #print(f"Final num: {cups.get_final_num()}")
    return cups.get_final_num()