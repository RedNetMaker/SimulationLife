import copy
import random

class Gen:
    letter:str
    correct:bool = False

    def __init__(self, letter):
        self.letter = letter

class Model:
    letters: str = " abcdefghijklmnopqrstuvwxyz"
    gens: list[Gen] = []
    count: int = 0
    replicate:bool = False

    def __init__(self, prefModelGens:list[Gen], initGens: list):
        self.gens = copy.deepcopy(prefModelGens)
        self.gens[random.randint(0, len(self.gens) - 1)].letter = random.choice(self.letters)

        for i in range(len(self.gens)):
            if self.gens[i].letter == initGens[i]:
                self.gens[i].correct = True
                self.count += 1
            else:
                self.gens[i].correct = False