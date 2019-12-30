from board import Board
from player import Player
from itertools import combinations, permutations
import heapq

class Solver():
    def __init__(self):
        self.validWords = set(open('dictionary.txt', 'r').read().split('\n'))

    def stringSubsets(self,s):
        s = sorted(s)
        return list(set([''.join(l) for i in range(len(s)) for l in combinations(s, i+1)]))

    def getCandidateWords(self,sets):
        ret = []
        for item in sets:
            if item in self.board.lookupDict:
                ret += self.board.lookupDict[item]
        return ret

    def solve(self,tiles,board: Board):
        self.candidates = []
        self.board = board
        self.tiles = tiles
        currLetters = tiles
        for i, row in enumerate(self.board.board):
            currLetters = ''.join(tiles + [x for x in row if x != ''])

            sets = self.stringSubsets(currLetters)
            validOptions = self.getCandidateWords(sets)

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

            sets = self.stringSubsets(currLetters)
            validOptions = self.getCandidateWords(currLetters)

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
