import os, sys
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
    # Takes forever to run
    def forward_propagate(self, game=None):
        game = game if game != None else self.game

        if self.startback(game.candidacy()):
            return False
        if np.count_nonzero(game.candidacy() == None) == 81:
            return game

        choices = game.best_choices()
        for r,c in zip(choices[0], choices[1]):
            G = copy.deepcopy(game)
            for nv in list(G.board[r,c].candidates):
                G.setCell(r,c,nv)
                Res = self.forward_propagate(G)
                if type(Res) == type(Board):
                    return Res
        return False
    
    # Raw iterative transaction
    # Does not complete task
    def iterative(self):
        for y in range(9):
            for x in range(9):
                if self.game.board[y,x].value == 0:
                    for v in self.game.board[y,x].candidates:
                        self.game.setCell(y,x,v)
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
        #print(self.game.candidacy())
        pass