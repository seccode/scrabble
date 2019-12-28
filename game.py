import numpy as np
import matplotlib.pyplot as plt
from board import Board
from player import Player

class Game():
    def __init__(self,numPlayers=2):
        self.numPlayers = numPlayers
        self.scoreBoard = np.zeros(numPlayers)
        self.board = Board()
        self.players = [Player(self.board) for _ in range(numPlayers)]
        self.turn = 0
    
    def startGame(self):
        for p in self.players:
            p.drawTiles()
        canMove = True
        while canMove:
            print("Player {} to move".format(self.turn+1))
            self.board.showBoard()

            moved = False
            while not moved:
                print(self.players[self.turn].tiles)
                word = input("Word to play: ")
                row = int(input("Row to play word: "))
                col = int(input("Column to play word: "))
                direction = input("Vertical (V) or Horizontal (H): ")[0].upper()
                print("\n")

                try:
                    self.players[self.turn].move(word,(row,col),across=(direction=='H'))
                    moved = True
                except Exception as e:
                    print("\nNot a valid move, try again [{}]\n".format(e))
                    continue

            self.scoreBoard[self.turn] = self.players[self.turn].score
            if self.turn == self.numPlayers - 1:
                self.turn = 0
            else:
                self.turn += 1
            print(self.scoreBoard)

if __name__ == "__main__":
    g = Game()
    g.startGame()














#
