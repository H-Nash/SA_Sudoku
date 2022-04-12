import os, sys

import numpy as np
import random as r
import time as t
import colorama as rgb

from Cell import Cell

class Board:
    def __init__(self, seed=None):
        self.R = r.Random().seed(t.time())
        self.board  = np.full((9,9),Cell())
        self.c_map = np.full((9,9),0) #for color mapping the output
        if seed is not None:
            self.__fill(seed)
        else:
            self.__fill(6)
    
    def __fill(self, seed):
        for i in range(seed):
            x = r.randrange(0,9)
            y = r.randrange(0,9)
            n = r.randrange(1,9)

            self.board[y,x] = Cell(n, static=True)
            
            iter = 1
            while(self.board_error() > 0):
                if iter%10 == 0:
                    self.board[y,x] = Cell()
                    x = r.randrange(0,9)
                    y = r.randrange(0,9)

                n = r.randrange(1,9)
                self.board[y,x].setState(n, True)
            self.c_map[y,x] = 1
        
    def peer_vertical(self, cell):
        x,y = cell #tuple
        temp = self.board[:,x].flatten()
        return list(temp)
    
    def peer_horizontal(self, cell):
        x,y = cell
        temp = self.board[y:,:].flatten()
        return list(temp)
    
    def peer_block(self, cell):
        x,y = cell
        bc0 = lambda c : 3*(c//3)
        bc1 = lambda c: 3*( (c//3) + 1 )
        temp = self.board[bc0(y):bc1(y)][bc0(x):bc1(x)].flatten()
        return list(temp)
    
    def cell_error(self, cell, gt = 0):
        coll = dict([(i,[]) for i in range(1,10)])
        region = self.peer_block(cell) + self.peer_vertical(cell) + self.peer_horizontal(cell)
        for elem in region:
            if(elem > Cell(gt)):
                coll[elem.getValue()].append(elem)
        return sum([len(c)-1 for c in coll.values()])
    
    def board_error(self, gt = Cell(0)):
        return sum([sum([self.cell_error((x,y)) for x in range(9)]) for y in range(9)])
        
    
    def colorize_errors(self, gt=None):
        for y in range(9):
            for x in range(9):
                if self.cell_error(x,y) > 0:
                    self.c_map[y,x] = 2
                else:
                    if self.c_map[y,x] != 1:
                        self.c_map[y,x] = 0
    def print(self, show_errors=False):
        colors = [rgb.Fore.WHITE, rgb.Fore.GREEN, rgb.Fore.RED]
        
        if show_errors:
            self.board_error(gt=Cell(0), color=True)

        for y in range(9):
            if y > 0 and y%3 == 0:
                print(colors[0]+''.join(['-' for i in range(21)]))

            for x in range(9):
                if x > 0 and x%3 == 0:
                    print(colors[0]+"|", end=" ")
                o = str(self.board[y,x]) if self.board[y,x] > BLANK else " "
                print(colors[self.c_map[y,x]] + o, end=" ")

            print()
        print(colors[0])

