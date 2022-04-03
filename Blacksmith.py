import os, sys
import math as m
import numpy as np

class Balcksmith:
    
    def __init__(self):
        pass

    def acceptance_probability(self, delta=0, temp=1):
        if type(delta) == type(int) and type(temp) == type(int):
            return -1 * (1/ (1+ m.exp(delta/temp)))
        
        return -1 * (1 / (1 + np.exp(delta/temp)))