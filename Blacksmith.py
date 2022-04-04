import os, sys
import math as m
import numpy as np
import random as r
import time as t

class Blacksmith:
    
    def __init__(self,game):
        self.game = game
        self.cost_hist = game.error_matrix()
        self.last_game = game.get_board()

        self.next_game = None
        self.next_cost = None

        self.mask_filter = game.get_mask()
        pass

    def acceptance_probability(self, delta=0, temp=1):
        if type(delta) == type(int) and type(temp) == type(int):
            return -1 * (1/ (1+ m.exp(delta/temp)))
        return -1 * (1 / (1 + np.exp(delta/temp)))
    
    def apply_mask(self):
        self.next_game = self.last_game + (np.random.randint(2,size=np.shape(self.last_game)) * np.abs(self.mask_filter-1))
    
    def new_cost(self):
        self.next_cost = self.game.error_matrix(board=self.next_game, cmap=self.mask_filter)
    


                    