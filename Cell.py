import os, sys
from xmlrpc.client import FastMarshaller

class Cell:
    def __init__(self, start_value):
        self.value = start_value
        self.candidates = set(list([i for i in range(1,10)]))
        self.probability = lambda: 1/len(self.candidates) if len(self.candidates) > 0 else -1
        self.static = False

    def setValue(self, value, u=False):
        if value in self.candidates:
            self.value = value
            if u == False:
                self.candidates = set()
        #self.candidates = self.drop(value)

    def put(self,value):
        self.candidates.add(value)

    def drop(self, value):
        if type(value) == type(set()):
            self.candidates -= value
            return
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
    def __lt__(self, other): return self.value < other.value