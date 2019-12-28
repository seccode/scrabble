import numpy as np
import matplotlib.pyplot as plt
from board import Board

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
                    neededPlayerTiles.append(word[x])
        else:
            for x, i in enumerate(range(position[0],position[0]+len(word))):
                if (i,position[1]) not in self.board.activeTiles:
                    neededPlayerTiles.append(word[x])
        
        return all([(letter.upper() in self.tiles) for letter in neededPlayerTiles]), neededPlayerTiles

    def move(self,word,position,across=True):
        res = self.canPlayWord(word, position, across=across)
        if not res[0]:
            raise Exception("Player does not have tiles sufficient for this move")
        self.score += self.board.placeWord(word,position,across=across)
        for letter in res[1]:
            self.tiles.remove(letter.upper())
        self.drawTiles()












#
