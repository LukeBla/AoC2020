'''
Created on 4 Dec 2020

@author: Luke
'''

import os
import socket

def set_wd(day):
    if socket.gethostname() == "madtop":
        base_dir="/home/luke/Dropbox/Programming/Projects/AdventOfCode/2020/AdventOfCode"
    else:
        base_dir='C:\\Users\\luke_\\Dropbox\\Programming\\Projects\\AdventOfCode\\2020\\AdventOfCode'
    os.chdir(os.path.join(base_dir, "AOC", f"day{day}"))
