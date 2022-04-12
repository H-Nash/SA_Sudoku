import os, sys
from Board import Board

if __name__ == "__main__":
    sudoku = Board()
    sudoku.populate(12)
    print(sudoku)