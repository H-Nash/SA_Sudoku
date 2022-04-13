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

<<<<<<< HEAD
    #steel.apply_mask()
    #print(steel.next_game)
    while(np.count_nonzero(sudoku.board == 0) > 0):
        steel.new_cost()
        sudoku.print(show_errors = True)
    #sudoku.cell_possibilities(3,4)
=======
    # print("Iterative:")
    # print(c.iterative())
    # print("*blanks imply I couldn\'t reach a decision")
    c.unique_candidates()
    print(c.iterative())
>>>>>>> 080df9d0a2cf94290c2af08a1c786556d708e2e2
