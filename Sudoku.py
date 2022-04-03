import os, sys
import numpy as np

from Board import Board

if __name__ == "__main__":
    sudoku = Board(20)  #max in reasonable time is 20
    sudoku.print(show_errors = True)