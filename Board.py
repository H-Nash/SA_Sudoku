import os, sys
import numpy as np
import random as r
import time as t

import colorama as rgb

BLANK = 0

# https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
class Board:
    def __init__(self, seed =None):
        self.R = r.Random().seed(t.time())
        self.board = np.full((9,9),0)
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

            self.board[y,x] = n
            
            iter = 1
            while(self.board_error(gt=BLANK) > 0):
                if iter%10 == 0:
                    self.board[y,x] = BLANK
                    x = r.randrange(0,9)
                    y = r.randrange(0,9)

                n = r.randrange(1,9)
                self.board[y,x] = n
            self.c_map[y,x] = 1
            
    
    def print(self, show_errors=False):
        colors = [rgb.Fore.WHITE, rgb.Fore.GREEN, rgb.Fore.RED]

        if show_errors:
            self.board_error(gt=BLANK, color=True)

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
        

    #HELPER functions
    def peer_horizon(self, cell, gt=None): # <-->
        x,y = cell #tuple
        temp = self.board[y,:]
        if gt is not None:
            temp = temp[temp>gt]
        return list(temp)
    
    def peer_vertical(self,cell, gt=None): # ^|v
        x,y = cell #tuple
        temp = self.board[:,x]
        if gt is not None:
            temp = temp[temp>gt]
        return list(temp)
    
    def peer_block(self,cell, gt=None): # get 3x3 grid segment :: return as 1d list
        x,y = cell #tuple
        bc0 = lambda c : 3*(c//3)
        bc1 = lambda c: 3*( (c//3) + 1 )
        temp = self.board[bc0(y):bc1(y)][bc0(x):bc1(x)].flatten()
        if gt is not None:
            temp = temp[temp>gt]
        return list(temp) 

    def error_check(self, region): # region take as list from peer functions
        return (len(region) - len(set(region)))
    
    # Sum of error from all regions for given cell
    def cell_error(self, x,y, gt=None):
        c = (x, y)
        regions = [self.peer_horizon(c, gt), self.peer_vertical(c, gt), self.peer_block(c, gt)]
        err_batt = sum([self.error_check(region) for region in regions])
        return err_batt

    def board_error(self, gt=None, color=False):
        o = sum([
            sum([
                self.cell_error(x,y, gt) for x in range(9)
                ]) for y in range(9)
        ])
        if color:
            self.colorize_errors(gt)
        return o
    
    def colorize_errors(self, gt=None):
        for y in range(9):
            for x in range(9):
                if self.cell_error(x,y, BLANK) > 0:
                    self.c_map[y,x] = 2
                else:
                    if self.c_map[y,x] != 1:
                        self.c_map[y,x] = 0
