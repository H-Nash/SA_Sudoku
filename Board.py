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
    
<<<<<<< HEAD
    def peer_block(self,cell, gt=None, board=None): # get 3x3 grid segment :: return as 1d list
        board = self.board if board is None else board

        x,y = cell #tuple
        bc0 = lambda c : 3*(c//3)
        bc1 = lambda c: 3*((c//3)+1)-1
        temp = board[bc0(y):bc1(y)][bc0(x):bc1(x)].flatten()
        if gt is not None:
            temp = temp[temp>gt]
        return list(temp) 

    def error_check(self, region): # region take as list from peer functions
        return (len(region) - len(set(region)))
    
    #Sum of error from all regions for given cell
    def cell_error(self, x,y, gt=None, board=None):
        board = self.board if board is None else board
        c = (x, y)
        regions = [self.peer_horizon(c, gt), self.peer_vertical(c, gt), self.peer_block(c, gt)]
        err_batt = sum([self.error_check(region) for region in regions])
        return err_batt
    
    def cell_possibilities(self, x, y, board=None):
        M = [i for i in range(1,10)]
        board = self.board if board is None else board
        c = (x, y)
        if board[y,x] > 0:
            return []
        regions = [self.peer_horizon(c, gt=0), self.peer_vertical(c, gt=0), self.peer_block(c, gt=0)]
        collect = set()
        for r in regions:
            collect = set(collect).union(set(r))
        collect = set(collect).symmetric_difference(set(M))
        return collect

    def board_error(self, gt=None, color=False):
        o = sum([
            sum([
                self.cell_error(x,y, gt) for x in range(9)
                ]) for y in range(9)
        ])
        if color:
            self.colorize_errors(gt)
        return o
=======
    def peers(self,r,c):
        b_s = lambda x: 3*(x//3)
        b_e = lambda x: 3*((x//3)+1)#-1
        return np.unique(np.concatenate((self.board[:,c].flatten(), self.board[r,:].flatten(), self.board[b_s(r):b_e(r),b_s(c):b_e(c)].flatten())))
    
    # Act on elements with best probability of conclusion
    def best_choices(self):
        pl = self.probability()
        pl = np.where(pl == pl.max())
        return pl

    def undo(self,r,c,v):
        self.board[r,c].setValue(0, u=True)
        b_s = lambda x: 3*(x//3)
        b_e = lambda x: 3*((x//3)+1)#-1

        # runtime of 9 instead of >27
        for k in range(9):
            self.board[k,c].put(v)
            self.board[r,k].put(v)
            self.board[b_s(r)+(k//3), b_s(c)+(k%3)].put(v)

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
>>>>>>> 080df9d0a2cf94290c2af08a1c786556d708e2e2
    
    def color_errors(self):
        for y in range(9):
            for x in range(9):
<<<<<<< HEAD
                if self.cell_error(x,y, BLANK) > 0:
                    self.c_map[y,x] = 2
                else:
                    if self.c_map[y,x] != 1:
                        self.c_map[y,x] = 0
    
    # def error_matrix(self, board=None, cmap=None):
    #     board = self.board if board is None else board
    #     cmap = self.c_map if cmap is None else cmap

    #     arr = np.asarray([
    #         [
    #             self.cell_error(x,y, board=board) for x in range(9)
    #             ] for y in range(9)
    #     ]) * (cmap - 1)
    #     return arr
    
    def prob_matrix(self, board=None, cmap=None):
        board = self.board if board is None else board
        cmap = self.c_map if cmap is None else cmap
        prob_arr = np.asarray([
            [
                list(self.cell_possibilities(x,y, board=board)) for x in range(9)
                ] for y in range(9)
        ])
        arr = np.asarray([ [ len(x) for x in y ] for y in prob_arr ]) * abs(cmap-1)
        return list([prob_arr, arr])
    
    def get_board(self):
        return self.board
    
    def get_mask(self):
        return self.c_map
    
    def value(self, x,y,v=None):
        if (x > -1 and x < 10) and (y > -1 and y < 10):
            if v is not None:
                self.board[y,x] = v
            else:
                return self.board[y,x]
=======
                if not self.board[y,x].static:
                    self.c_map[y,x] = 2 if -self.erroneous(y,x) else 0

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
>>>>>>> 080df9d0a2cf94290c2af08a1c786556d708e2e2
