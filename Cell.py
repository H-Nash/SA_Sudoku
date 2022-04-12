import os, sys

class Cell:
    def __init__(self, value = 0, static=False):
        self.static = static
        self.value = value
        self.crook = list()
    
    def drop(self, value):
        self.crook = self.crook.remove(value)
    
    def crook(self, values):
        self.crook = values
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value
    
    def setState(self, value, static):
        self.value = value
        self.static = static

    def is_static(self):
        return self.static
    
    def __gt__(self, other):
        return self.value > other.value
    def __gte__(self, other):
        return self.value >= other.value
    
    def __lt__(self, other):
        return self.value < other.value
    def __lte__(self, other):
        return self.value <= other.value
    
    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.value == other.value
    def __ne__(self, other):
        return self.value != other.value
    
    def __hash__(self):
        return hash(self.value)