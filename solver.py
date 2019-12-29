from board import Board
from player import Player
from itertools import combinations
import heapq

class Solver():
    def solve(self,tiles,board: Board):
        self.candidates = []
        self.board = board
        self.tiles = tiles
        currLetters = tiles
        for i, row in enumerate(self.board.board):
            currLetters = ''.join(tiles + [x for x in row if x != ''])
            options = [''.join(l) for i in range(len(currLetters),0,-1)
                        for l in combinations(currLetters,i)]
            validOptions = [x for x in options if self.board.checkValidWord(x)]
            for j in range(self.board.size):
                for word in validOptions:
                    player = Player(self.board)
                    if player.canPlayWord(word, (i, j), across=True, tiles=tiles)[0]:
                        try:
                            score = self.board.findScore(word,(i,j),across=True,place=False)
                            heapq.heappush(self.candidates, (-score, word, (i,j), True))
                        except:
                            pass

        for j, col in enumerate(self.board.board.T):
            currLetters = ''.join(tiles + [x for x in col if x != ''])
            options = [''.join(l) for i in range(len(currLetters), 0, -1)
                        for l in combinations(currLetters, i)]
            validOptions = [x for x in options if self.board.checkValidWord(x)]

            for i in range(self.board.size):
                for word in validOptions:
                    player = Player(self.board)
                    if player.canPlayWord(word, (i, j), across=False, tiles=tiles)[0]:
                        try:
                            score = self.board.findScore(word, (i, j), across=False, place=False)
                            heapq.heappush(self.candidates, (-score, word, (i, j), False))
                        except:
                            pass

        if len(self.candidates) > 0:
            return heapq.heappop(self.candidates)
        return None

if __name__ == "__main__":
    b = Board()
    b.placeWord("person",(7,4))
    s = Solver()
    res = s.solve(['A', 'B', 'C', 'D', 'E', 'D', 'E'], b)
    b.placeWord(res[1],res[2],across=res[3])
    b.showBoard()
























#
