import os, sys
import math as m
import numpy as np
import random as r
import time as t

class Blacksmith:
    
    def __init__(self,game):
        self.cost_hist = game.error_matrix()
        self.last_game = game.get_board()
        pass

    def acceptance_probability(self, delta=0, temp=1):
        if type(delta) == type(int) and type(temp) == type(int):
            return -1 * (1/ (1+ m.exp(delta/temp)))
        return -1 * (1 / (1 + np.exp(delta/temp)))
    
    

                    