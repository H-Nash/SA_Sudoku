import os, sys
from Board import Board
from Crook import Crook
import copy
from Simplified import SimpleSolver
import numpy as np
from LinearProgram import Linear

if __name__ == "__main__":
    sudoku = Board()
    sudoku.populate(12)
    print(sudoku)
    
    s = SimpleSolver(sudoku)
    print(sudoku)