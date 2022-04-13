import os, sys
import numpy as np

class SimpleSolver:
    def __init__(self, game):
        grid = game.getBoard()
        if self.sudokuSolver(grid):
            game.apply_solution(grid)

    def rowCheck(self,grid,row,val):
        for j in range(9):
            if val==grid[row][j]:
                return False
        return True

    def colCheck(self,grid,col,val):
        for r in range(9):
            if val==grid[r][col]:
                return False
        return True

    def boxCheck(self,grid,row,col,val):
        r=(row//3)*3+1
        c=(col//3)*3+1
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if grid[r+i][c+j]==val:
                    return False
        return True

    def findUnassigned(self,grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j]==0:
                    return i,j
        return -1,-1

    def sudokuSolver(self, grid):
        i,j=self.findUnassigned(grid)
        if i==-1 and j==-1:
            return True

        for num in range(1,10): #ignore candidacy to simplify depth
            if self.rowCheck(grid,i,num) and self.colCheck(grid,j,num) and self.boxCheck(grid,i,j,num):
                grid[i][j]=num
                if self.sudokuSolver(grid):
                    return True
                grid[i][j]=0
        return False

grid=[
    [".","8",".","5","3",".","2","7","6"],
    [".","5",".","6",".",".",".",".","."],
    ["6","1","3",".",".",".",".",".","."],
    [".",".","6",".","5",".",".",".","."],
    [".","3","2",".",".",".","7",".","1"],
    ["7","4","5",".",".","8","6","9","3"],
    [".","7",".","9","6",".","5",".","."],
    ["4",".",".","1","8",".",".","6","7"],
    ["5",".",".",".",".","4","8","2","9"]
]