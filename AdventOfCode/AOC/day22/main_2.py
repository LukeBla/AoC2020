'''
Created on 22 Dec 2020

@author: Luke
'''



from AOC.config import config
config.set_wd(22)


class Player(object):
    def __init__(self, _id, deck):
        # Index 0 = top of deck
        self.deck = deck
        self.id = _id

    def can_play(self):
        """
        Can play if top card of deck at least as large as
        number of cards left
        """
        return bool(self.deck)
        
        
    def get_next(self):
        if self.deck:
            return self.deck.pop(0)
        else:
            return None
        
    def add_cards(self, winner, loser):
        """
        Add back to deck - highest card on top
        """
        self.deck.extend([winner, loser])
        
    def get_score(self):
        
        return sum([ a*b for (a, b) in zip(self.deck, range(len(self.deck), 0, -1))])
    
    
class Game(object):
    def __init__(self, p1_deck, p2_deck, level=0):
        self.p1 = Player(1, p1_deck)
        self.p2 = Player(2, p2_deck)
        self.previous_round_hashes = set()
        self.level = level
        #print("."*level)
    
    def get_hash(self, p1, p2):
        return (hash(tuple(p1.deck)), hash(tuple(p2.deck)))
    
    def play(self):
        self.playing = True
        self.winner = None
        while self.playing:
            self.next_round()
        return self.winner
    
    def next_round(self):
        round_hash = self.get_hash(self.p1, self.p2)
        if round_hash in self.previous_round_hashes:
            self.playing = False
            self.winner = self.p1
            return
        else:
            self.previous_round_hashes.add(round_hash)
        
        if not self.p1.can_play():
            self.playing = False
            self.winner = self.p2
            return
        elif not self.p2.can_play():
            self.playing = False
            self.winner = self.p1
            return
        
        p1_card = self.p1.get_next()
        p2_card = self.p2.get_next()
        if p1_card > len(self.p1.deck) or p2_card > len(self.p2.deck):
            if p1_card > p2_card:
                self.p1.add_cards(p1_card, p2_card)
            else:
                self.p2.add_cards(p2_card, p1_card)
        else:
            subgame = Game(self.p1.deck[:p1_card], self.p2.deck[:p2_card], self.level+1)
            winner = subgame.play().id
            if winner == 1:
                self.p1.add_cards(p1_card, p2_card)
            else:
                self.p2.add_cards(p2_card, p1_card)
            
def get_input(input_type):
    if input_type == "test":
        ret = [[9, 2, 6, 3, 1], [5, 8, 4, 7, 10]]
    else:
        with open("input.txt") as f:
            p1_deck = []
            p2_deck = []
            header = next(f).strip()
            if header != "Player 1:":
                raise RuntimeError(f"Expected Player 1: header - got {header}")
            while True:
                line = next(f).strip()
                if line == "": break
                p1_deck.append(int(line))
                
            header = next(f).strip()
            if header != "Player 2:":
                raise RuntimeError(f"Expected Player 2: header - got {header}")
            while True:
                try:
                    line = next(f).strip()
                except StopIteration:
                    break
                p2_deck.append(int(line))
        ret = [p1_deck, p2_deck]
    return ret

def run(input_type):
    (p1_deck, p2_deck) = get_input(input_type)
    game = Game(p1_deck, p2_deck)
    winner = game.play()
    print(winner.id, winner.get_score())
