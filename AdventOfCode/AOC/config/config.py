'''
Created on 4 Dec 2020

@author: Luke
'''

import os

def set_wd(day):
    base_dir='C:\\Users\\luke_\\Dropbox\\Programming\\Projects\\AdventOfCode\\2020\\AdventOfCode'
    os.chdir(os.path.join(base_dir, "AOC", f"day{day}"))