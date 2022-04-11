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
    def peer_horizon(self, cell, gt=None, board=None): # <-->
        board = self.board if board is None else board

        x,y = cell #tuple
        temp = board[y,:]
        if gt is not None:
            temp = temp[temp>gt]
        return list(temp)
    
    def peer_vertical(self,cell, gt=None, board=None): # ^|v
        board = self.board if board is None else board

        x,y = cell #tuple
        temp = board[:,x]
        if gt is not None:
            temp = temp[temp>gt]
        return list(temp)
    
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
    
    def colorize_errors(self, gt=None):
        for y in range(9):
            for x in range(9):
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
