import numpy as np
from board import Board
from player import Player
from solver import Solver
import sys
import argparse

class Game():
    def __init__(self, numPlayers=2, CPUCount=1):
        self.numPlayers = numPlayers
        self.CPUCount = CPUCount
        self.scoreBoard = np.zeros(numPlayers)
        self.board = Board()
        self.players = [Player(self.board) for _ in range(numPlayers)]
        for p in self.players:
            p.drawTiles()
        self.turn = 0
        self.solver = Solver()
        self.CPUTurns = [True]*CPUCount + [False]*(numPlayers-CPUCount)
    
    def startGame(self):
        canMove = [True]*self.numPlayers
        while any(canMove) and all([(len(x.tiles) > 0) for x in self.players]):
            self.board.showBoard(tiles=[p.tiles for p in self.players],scores=self.scoreBoard)

            moved = False
            while not moved:

                print("Player {} to move".format(self.turn+1))

                # CPU
                if self.CPUTurns[self.turn]:
                    bestMove = self.solver.solve(self.players[self.turn].tiles,self.board)
                    if not bestMove:
                        canMove[self.turn] = False
                        print("Can't move, pass")
                        break
                    canMove = [True]*self.numPlayers

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

                try:
                    points = self.players[self.turn].move(word,(row,col),across=(direction=='H'))
                    moved = True
                    print("Player {} played {} for {} points".format(self.turn + 1,word,points))
                except Exception as e:
                    print("\nNot a valid move, try again [{}]\n".format(e))
                    continue

            self.scoreBoard[self.turn] = self.players[self.turn].score
            if self.turn == self.numPlayers - 1:
                self.turn = 0
            else:
                self.turn += 1
        
        print("\n\nFinal Score: {}".format(self.scoreBoard))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--players',dest='players',type=int,default=2)
    parser.add_argument('--CPU',dest='CPU',type=int,default=1)
    args = parser.parse_args()
    
    assert args.players > 0 and args.players <= 5, "Number of players must be between 1-4"
    assert args.CPU <= args.players, "Number of CPU players must be less than or equal to number of players"
    assert args.CPU >= 0, "Number of CPU players must be greater than or equal to 0"

    g = Game(numPlayers=args.players,CPUCount=args.CPU)
    g.startGame()














#
