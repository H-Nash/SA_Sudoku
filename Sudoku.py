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
    
    # Using Crook's
    # s = SimpleSolver(sudoku)
    # print(sudoku)

    # Using Linear Programming

    l = Linear(sudoku)
    l.solve()
    l.apply_solution()
    print(sudoku)
    