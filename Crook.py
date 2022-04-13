from operator import truediv
import os, sys
from turtle import Turtle
import numpy as np
import copy

from Board import Board
from Cell import Cell

class Crook:
    def __init__(self, game):
        self.game = game
        pass
    
    # if an unmarked cell has no candidates, 
    # then we have invalidated our sudoku and 
    # need to work back to a safe space
    def startback(self, cand):
        return np.count_nonzero(cand == 0) > 0
    
    # Brute force Depth First Search (Crook's)
    def recursive(self, game=None, r=0,c=0):
        game = game if game != None else self.game
        if game.board[r,c].value == 0:
            V = 0
            v = game.board[r,c].candidates
            while(len(v) > 0):
                game.setCell(r,c,V)
                if np.count_nonzero(game.candidacy() == 0) > 0:
                    game.board.undo(r,c,V)
                elif game.board[r,c].value != 0:
                    state = self.recursive(copy.deepcopy(game),(r+1 if (c+1)%9 == 0 else r ),(c+1)%9)
                    if state == False:
                        game.board.undo(r,c,V)
                    if state != False:
                        return state
        return game
    
    def backtracking(self, game=None):
        game = game if game != None else self.game
        RC = game.best_choices()
        if RC == None:
            return True
        for r,c in zip(RC[0],RC[1]):
            for v in game.board[r,c].candidates:
                if game.valid(r,c,v):
                    game.setCell(r,c,v)
                if self.backtracking():
                    return True
                game.undo(r,c,v)
        return False


    
    # Raw iterative transaction
    def iterative(self):
        for y in range(9):
            for x in range(9):
                if self.game.board[y,x].value == 0:
                    for v in self.game.board[y,x].candidates:
                        self.game.setCell(y,x,v)
                        print(np.count_nonzero(self.game.candidacy() == 0))
                        if self.game.board[y,x].value != 0:
                            break
                        else:
                            self.game.undo(y,x,v)
        return self.game

    def unique_candidates(self):
        for y in range(9):
            for x in range(9):
                peers = self.game.peers(y,x)
                peer_sets = [p.candidates for p in peers]
                major = set()
                for ps in peer_sets:
                    major.union(ps)
                inter = self.game.board[y,x].candidates.intersection(major)
                core = self.game.board[y,x].candidates - inter
                self.game.board[y,x].candidates = core
        pass