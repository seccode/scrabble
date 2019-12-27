import numpy as np
import matplotlib.pyplot as plt


class Board():
    def __init__(self,size=15):
        self.size = size
        self.board = np.full(shape=(size,size),fill_value='')
        self.tilesLeft = 100
        self.tileScores = {
                            ' ':0,
                            'A':1,
                            'B':3,
                            'C':4,
                            'D':2,
                            'E':1,
                            'F':4,
                            'G':2,
                            'H':4,
                            'I':1,
                            'J':8,
                            'K':5,
                            'L':1,
                            'M':3,
                            'N':1,
                            'O':1,
                            'P':3,
                            'Q':10,
                            'R':1,
                            'S':1,
                            'T':1,
                            'U':1,
                            'V':4,
                            'W':4,
                            'X':8,
                            'Y':4,
                            'Z':10,
                            }
        self.tileCount = {
                    ' ':2,
                    'A':9,
                    'B':2,
                    'C':2,
                    'D':4,
                    'E':2,
                    'F':2,
                    'G':3,
                    'H':2,
                    'I':9,
                    'J':1,
                    'K':1,
                    'L':4,
                    'M':2,
                    'N':6,
                    'O':8,
                    'P':2,
                    'Q':1,
                    'R':6,
                    'S':4,
                    'T':6,
                    'U':4,
                    'V':2,
                    'W':2,
                    'X':1,
                    'Y':2,
                    'Z':1,
                    }
        self.tiles = []
        for key, value in self.tileCount.items():
            self.tiles += [key]*value
        np.random.shuffle(self.tiles)
        self.validWords = set(open('dictionary.txt','r').read().split('\n'))

    def pickTile(self):
        # Randomly pick tile and remove from tile set
        ret = self.tiles.pop()
        self.tileCount[ret] -= 1
        self.tilesLeft -= 1
        return ret

    def expandPosition(self,letter,position,across=True):
        # Find vertical or horizontal sequence of letters at this position
        if across:
            t, b = position[0], position[0]
            while t > 0 and b < self.board.shape[0] - 1:
                if self.board[t-1,position[1]] != '' and self.board[b+1,position[1]] != '':
                    t -= 1
                    b += 1
                elif self.board[t-1,position[1]] != '':
                    t -= 1
                elif self.board[b+1,position[1]] != '':
                    b += 1
                else:
                    break
            word = ''.join(self.board[t:position[0],position[1]]) + letter + ''.join(self.board[position[0]+1:b,position[1]])
        else:
            l, r = position[1], position[1]
            while l > 0 and r < self.board.shape[1] - 1:
                if self.board[l-1,position[0]] != '' and self.board[r+1,position[0]] != '':
                    l -= 1
                    r += 1
                elif self.board[l-1,position[0]] != '':
                    l -= 1
                elif self.board[b+1,position[0]] != '':
                    r += 1
                else:
                    break
            word = ''.join(self.board[position[0], l:position[1]]) + letter + ''.join(self.board[position[0], r+1:position[1]])
        return word

    def checkValidWord(self,word):
        # Check if a word is in official scrabble dictionary
        return word.upper() in self.validWords
    
    def checkWordPlacement(self,word,position,across=True):
        # Check if given word can be placed on board in given position
        assert self.checkValidWord(word), "Word is not valid"

        # Check validity of all words that are created by touching this word
        wordList = []
        if across:
            for x, i in enumerate(range(position[1],position[1] + len(word))):
                res = self.expandPosition(word[x],(position[0],i),across=True)
                print(res)
                if len(res) > 1:
                    wordList.append(res)
        else:
            for x, j in enumerate(range(position[0],position[0] + len(word))):
                res = self.expandPosition(word[x],(j,position[1]),across=False)
                print(res)
                if len(res) > 1:
                    wordList.append(res)
        return all([self.checkValidWord(x) for x in wordList])

    
    def placeWord(self,word,position,across=True):
        # Place word on board
        assert self.checkWordPlacement(word,position,across=across), "Word cannot be placed on board"

        if across:
            for x, i in enumerate(range(position[1],position[1] + len(word))):
                self.board[position[0],i] = word[x]
        else:
            for x, j in enumerate(range(position[0], position[0] + len(word))):
                self.board[j,position[1]] = word[x]
    
    def test(self,word,position,across=True):
        if across:
            for x, i in enumerate(range(position[1], position[1] + len(word))):
                self.board[position[0], i] = word[x]
        else:
            for x, j in enumerate(range(position[0], position[0] + len(word))):
                self.board[j, position[1]] = word[x]

        
# b = Board()
















#
