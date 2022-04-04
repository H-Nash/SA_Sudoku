import os, sys
import numpy as np

from Board import Board
from Blacksmith import Blacksmith

if __name__ == "__main__":
    sudoku = Board(6)  #max in reasonable time is 20
    sudoku.print(show_errors = True)

    steel = Blacksmith(sudoku)

    steel.apply_mask()
    print(steel.next_game)
    steel.new_cost()
    print(steel.next_cost)