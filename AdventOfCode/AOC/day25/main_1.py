'''
Created on 26 Dec 2020

@author: Luke
'''

SUBJECT = 7

def transform(val, subject):
    return (val * subject) % 20201227

def run_loop(loop_size, subject):
    val = 1
    for _ in range(loop_size):
        val = transform(val, subject)
    return val

def get_loop(key, subject):
    val = 1
    loop_size = 0
    while True:
        loop_size += 1
        val = transform(val, subject)
        if val == key: return loop_size
    raise RuntimeError("Could not find loop number")
    

def get_input(input_type):
    if input_type == "test":
        ret = [5764801, 17807724]
    else:
        ret = [6930903, 19716708]
    return ret

def run(input_type):
    (card_key, door_key) = get_input(input_type)
    card_loop_no = get_loop(card_key, 7)
    door_loop_no = get_loop(door_key, 7)
    card_encrypt_1 = run_loop(card_loop_no, door_key)
    card_encrypt_2 = run_loop(door_loop_no, card_key)
    assert card_encrypt_1 == card_encrypt_2, f"Differenct encryptions - {card_encrypt_1}, {card_encrypt_2}"
    return card_encrypt_1