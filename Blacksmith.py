import os, sys
import math as m
import numpy as np
import random as r
import time as t

class Blacksmith:
    
    def __init__(self,game):
        self.game = game
        #self.cost_hist = game.error_matrix()
        #self.last_game = game.get_board()

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
        self.nexts, self.next_cost = self.game.prob_matrix(cmap=self.mask_filter)
        y,x = np.where( self.next_cost == self.next_cost[self.next_cost > 0].min())
        #print(self.next_cost)
        for l in range(len(x)):
            for v in self.nexts[y[l],x[l]]:
                self.game.value(x[l],y[l],v)
                if(self.game.cell_error(x[l],y[l], gt=0) > 0):
                    self.game.value(x[l],y[l],0)
                else:
                    return
            self.game.value(x[l],y[l],0)
        #self.next_state = self.next_cost[self.next_cost > np.where(self.next_cost == self.next_cost[self.next_cost > 0])]


                    