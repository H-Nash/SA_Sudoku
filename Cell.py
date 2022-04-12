import os, sys

class Cell:
    def __init__(self, start_value):
        self.value = start_value
        self.candidates = set(list([i for i in range(1,10)]))
        self.probability = lambda: 1/len(self.candidates) if len(self.candidates) > 0 else -1
        self.static = False

    def setValue(self, value):
        if value in self.candidates:
            self.value = value
            self.candidates.remove(value)
        #self.candidates = self.drop(value)

    def drop(self, value):
        try:
            self.candidates.remove(value)
        except KeyError:
            pass
    
    def proplen(self):
        try:
            return (len(self.candidates) if self.value == 0 else None)
        except (TypeError,):
            return -1
    
    def __eq__(self, other):
        if type(other) == type(int()):
            return self.value == other
        elif type(other) == type(Cell):
            return self.value == other.value

    def __hash__(self):
        return hash(self.value)