import os, sys
import numpy as np

# https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python
class Board:
    def __init__(self):
        self.board = np.full((9,9),0)
        __fill()
    
    def __fill(self, seed):
        pass

    #HELPER functions
    def peer_horizon(self, cell): # <-->
        x,y = cell #tuple
        return self.board[y][:]
    
    def peer_vertical(self,cell): # ^|v
        x,y = cell #tuple
        return self.board[:][x]
    
    def peer_block(self,cell): # get 3x3 grid segment :: return as 1d list
        x,y = cell #tuple
        bc0 = lambda c : 3*(c//3)
        bc1 = lambda c: 3*( (c//3) + 1 )
        return list(self.board[bc0(y):bc1(y)][bc0(x):bc1(x)].flatten()) # flatten and translate to list