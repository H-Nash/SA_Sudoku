import os, sys
from Board import Board
from Crook import Crook
import copy
import numpy as np

if __name__ == "__main__":
    sudoku = Board()
    sudoku.populate(12)
    print(sudoku)
    
    c = Crook(sudoku)
    # Too long
    #print(c.forward_propagate())

    # print("Iterative:")
    # print(c.iterative())
    # print("*blanks imply I couldn\'t reach a decision")
    c.unique_candidates()
    print(c.iterative())