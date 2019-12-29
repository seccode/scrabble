import numpy as np
from board import Board
from player import Player
from solver import Solver
import sys

class Game():
    def __init__(self,numPlayers=2):
        self.numPlayers = numPlayers
        self.scoreBoard = np.zeros(numPlayers)
        self.board = Board()
        self.players = [Player(self.board) for _ in range(numPlayers)]
        for p in self.players:
            p.drawTiles()

        self.turn = 0
        self.solver = Solver()
    
    def startGame(self):
        canMove = [True]*self.numPlayers
        while any(canMove) and all([(len(x.tiles) > 0) for x in self.players]):
            print("Player {} to move".format(self.turn+1))
            self.board.showBoard(tiles=[p.tiles for p in self.players],scores=self.scoreBoard)

            moved = False
            while not moved:

                # CPU
                # if self.turn % 2 == 0:
                if True:
                    bestMove = self.solver.solve(self.players[self.turn].tiles,self.board)
                    if not bestMove:
                        canMove[self.turn] = False
                        print("Can't move, pass")
                        break
                    canMove = [True]*self.numPlayers

                    print(-bestMove[0])
                    word = bestMove[1]
                    row = bestMove[2][0]
                    col = bestMove[2][1]
                    direction = {True:'H',False:'V'}[bestMove[3]]
                # Human
                else:
                    word = input("Word to play: ").upper()
                    while ' ' in word:
                        word.remove(' ')
                    row = int(input("Row to play word: "))
                    col = int(input("Column to play word: "))
                    direction = input("Vertical (V) or Horizontal (H): ")[0].upper()
                    print("\n")

                # try:
                print(word,(row,col),direction)
                self.players[self.turn].move(word,(row,col),across=(direction=='H'))
                moved = True
                # except Exception as e:
                #     print("\nNot a valid move, try again [{}]\n".format(e))
                #     continue

            self.scoreBoard[self.turn] = self.players[self.turn].score
            if self.turn == self.numPlayers - 1:
                self.turn = 0
            else:
                self.turn += 1
        
        print("\n\nFinal Score: {}".format(self.scoreBoard))

if __name__ == "__main__":
    g = Game(numPlayers=2)
    g.startGame()














#
