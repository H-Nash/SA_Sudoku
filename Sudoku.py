import os, sys
from Board import Board
from Crook import Crook
import copy

if __name__ == "__main__":
    sudoku = Board()
    sudoku.populate(12)
    print(sudoku)
    
    c = Crook(sudoku)
    #print(c.forward_propagate())
    print(c.iterative())