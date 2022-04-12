import os, sys
from pydoc import Doc
import numpy as np
import random as R
import time as t
import colorama as rgb
import copy

from Cell import Cell

class Board:
    def __init__(self):
        vCell = np.vectorize(Cell)
        self.board = vCell(np.full((9,9), 0))
        self.c_map = np.full((9,9), 0)
        rgb.init()
        self.colors = [rgb.Fore.WHITE, rgb.Fore.GREEN, rgb.Fore.RED]

    def populate(self, seed=6):
        R.seed(t.time())
        for s in range(seed):
            r = R.randrange(0,9)
            c = R.randrange(0,9)
            self.c_map[r,c] = 1
            while(self.board[r,c] == 0):
                v = R.randrange(1,10)
                self.setCell(r,c,v)
                self.board[r,c].static = True
    
    def probability(self):
        L = np.asarray([[(self.board[y,x].probability() if self.board[y,x].value == 0 else -1) for x in range(9)] for y in range(9)])
        return L
    
    # Act on elements with best probability of conclusion
    def best_choices(self):
        pl = self.probability()
        pl = np.where(pl == pl.max())
        return pl

    def setCell(self, r, c, v):
        self.board[r,c].setValue(v)
        b_s = lambda x: 3*(x//3)
        b_e = lambda x: 3*((x//3)+1)#-1

        # runtime of 9 instead of >27
        for k in range(9):
            self.board[k,c].drop(v)
            self.board[r,k].drop(v)
            self.board[b_s(r)+(k//3), b_s(c)+(k%3)].drop(v)
    
    def erroneous(self, r,c):
        b_s = lambda x: 3*(x//3)
        b_e = lambda x: 3*((x//3)+1)

        v,h,b = [self.board[:,c].flatten(), self.board[r,:].flatten(), self.board[b_s(r):b_e(r),b_s(c):b_e(c)].flatten()]
        V = (set(v) == len(v))
        H = (set(h) == len(h))
        B = (set(b) == len(b))
        return V and H and B

    
    def candidacy(self):
        L = np.asarray([[self.board[y,x].proplen() for x in range(9)] for y in range(9)])
        return L
    
    def color_errors(self):
        for y in range(9):
            for x in range(9):
                if not self.board[y,x].static:
                    self.c_map[y,x] = 2 if self.erroneous(y,x) else 0

    def __str__(self):
        self.color_errors()
        L = ""
        for y in range(9):
            for x in range(9):
                if x > 0 and x%3 == 0:
                    L += "| "
                L += (self.colors[self.c_map[y,x]] + str(self.board[y,x].value) + self.colors[0] if self.board[y,x].value > 0 else " ") + " "
            L += '\n' + (''.join(["-" for i in range(21)]) + "\n" if y<8 and (y+1)%3 == 0 else "")
        return L
