import numpy as np
import matplotlib.pyplot as plt
from board import Board
from collections import Counter

class Player():
    def __init__(self,board):
        self.tiles = []
        self.score = 0
        self.board = board

    def drawTiles(self):
        while len(self.tiles) < 7 and self.board.tilesLeft != 0:
            self.tiles.append(self.board.pickTile())

    def canPlayWord(self,word,position,across=True):
        neededPlayerTiles = []
        if across:
            for x, j in enumerate(range(position[1],position[1]+len(word))):
                if (position[0],j) not in self.board.activeTiles:
                    neededPlayerTiles.append(word[x].upper())
        else:
            for x, i in enumerate(range(position[0],position[0]+len(word))):
                if (i,position[1]) not in self.board.activeTiles:
                    neededPlayerTiles.append(word[x].upper())
        
        n = Counter(neededPlayerTiles)
        h = Counter(self.tiles)
        missing = []
        for key, value in n.items():
            if key not in h:
                missing += [key]*value
            else:
                if h[key] < value:
                    missing += [key]*(value - h[key])

        return (len(missing) <= h[' ']), neededPlayerTiles, missing

    def move(self,word,position,across=True):
        res = self.canPlayWord(word, position, across=across)
        if not res[0]:
            raise Exception("Player does not have tiles sufficient for this move")

        blanks = {}
        if len(res[2]) > 0:
            for x, letter in enumerate(word):
                if letter in res[2]:
                    res[2].remove(letter)
                    blanks[(position[0]+x*(not across),position[1]+x*(across))] = letter

        self.score += self.board.placeWord(word,position,across=across,blanks=blanks)
        for letter in res[1]:
            if letter in self.tiles:
                self.tiles.remove(letter.upper())
            else:
                self.tiles.remove(' ')
        self.drawTiles()












#
