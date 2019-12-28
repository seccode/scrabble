import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

        # Tile bonuses
        self.doubleLetters = set([(0,3),(0,11),(2,6),(2,8),(3,0),(3,7),(3,14),(6,2),(6,6),(6,8),(6,12),(7,3),(7,11),
                                (14,3),(14,11),(12,6),(12,8),(11,0),(11,7),(11,14),(8,2),(8,6),(8,8),(8,12)])
        self.tripleLetters = set([(1,5),(1,9),(5,1),(5,5),(5,9),(5,13),(13,5),(13,9),(9,1),(9,5),(9,9),(9,13)])
        self.doubleWords = set([(7,7),(1,1),(2,2),(3,3),(4,4),(13,13),(12,12),(11,11),(10,10),
                                (1,13),(2,12),(3,11),(4,10),(13,1),(12,2),(11,3),(10,4)])
        self.tripleWords = set([(0,0),(0,14),(14,14),(14,0),(7,0),(0,7),(14,7),(7,14)])

        self.activeTiles = {}

    def pickTile(self):
        # Randomly pick tile and remove from tile set
        ret = self.tiles.pop()
        self.tileCount[ret] -= 1
        self.tilesLeft -= 1
        return ret

    def showBoard(self):
        fig, ax = plt.subplots(1,figsize=(8,8))
        plt.axis("off")
        ax.set_xlim(-15,self.size*10 + 15)
        ax.set_ylim(-15,self.size*10 + 15)
        plt.gca().set_aspect('equal', adjustable='box')

        for x in range(self.board.shape[0]):
            ax.annotate(str(x), (x*10 + 5, self.size*10 + 14), color='black',
                        weight='bold', fontsize=12, ha='center', va='center')
            ax.annotate(str(x), (-5, self.size*10 - x*10 + 5), color='black',
                        weight='bold', fontsize=12, ha='center', va='center')
        
        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                tileColor = 'bisque'
                text = ''
                color = 'black'
                weight = 8
                subtext = ''
                if self.board[i,j] != '':
                    tileColor = 'peru'
                    text = self.board[i,j].upper()
                    color = 'white'
                    weight = 15
                    subtext = self.tileScores[text]
                elif (i,j) in self.doubleLetters:
                    tileColor = 'lightskyblue'
                    text = 'DL'
                elif (i,j) in self.tripleLetters:
                    tileColor = 'royalblue'
                    text = 'TL'
                elif (i, j) in self.doubleWords:
                    tileColor = 'plum'
                    if (i, j) != (7, 7):
                        text = 'DW'
                elif (i,j) in self.tripleWords:
                    tileColor = 'tomato'
                    text = 'TW'
                rect = Rectangle((j*10,self.size*10 - i*10),10,10,linewidth=1,edgecolor='k',facecolor=tileColor)
                ax.add_patch(rect)

                ax.annotate(text, (j*10 + 5, self.size*10 - i*10 + 5), color=color,
                            weight='bold', fontsize=weight, ha='center', va='center')
                ax.annotate(subtext, (j*10 + 8, self.size*10 - i*10 + 2), color=color,
                            weight='bold', fontsize=6, ha='center', va='center')

        # Add star at middle
        if (7,7) not in self.activeTiles:
            ax.scatter(75,85,marker='*',s=400,c='k',zorder=100)

        plt.show()

    def expandPosition(self,letter,position,across=True):
        # Find vertical or horizontal sequence of letters at this position
        if across:
            t, b = position[0], position[0]
            while t > 0:
                if self.board[t-1,position[1]] != '':
                    t -= 1
                else:
                    break
            while b < self.board.shape[0] - 1:
                if self.board[b+1,position[1]] != '':
                    b += 1
                else:
                    break
            word = ''.join(self.board[t:position[0],position[1]]) + letter + ''.join(self.board[position[0]+1:b,position[1]])
        else:
            l, r = position[1], position[1]
            while l > 0:
                if self.board[l-1,position[0]] != '':
                    l -= 1
                else:
                    break
            while r < self.board.shape[1] - 1:
                if self.board[r+1,position[0]] != '':
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
        assert self.checkValidWord(word), "'{}' is not a valid word".format(word)

        # Check validity of all words that are created by touching this word
        wordList = []
        if across:
            for x, i in enumerate(range(position[1],position[1] + len(word))):
                res = self.expandPosition(word[x],(position[0],i),across=True)
                if len(res) > 1:
                    wordList.append(res)
        else:
            for x, j in enumerate(range(position[0],position[0] + len(word))):
                res = self.expandPosition(word[x],(j,position[1]),across=False)
                if len(res) > 1:
                    wordList.append(res)
        return all([self.checkValidWord(x) for x in wordList])
    
    def tabulateScore(self,letter,score,position,bonus):
        if position in self.activeTiles:
            score += self.tileScores[self.board[position[0],position[1]]]
        elif position in self.doubleLetters:
            score += 2 * self.tileScores[letter]
        elif position in self.tripleLetters:
            score += 3 * self.tileScores[letter]
        elif position in self.doubleWords:
            score += self.tileScores[letter]
            bonus[2] += 1
        elif position in self.tripleWords:
            score += self.tileScores[letter]
            bonus[3] += 1
        else:
            score += self.tileScores[letter]
        return (score, bonus)
    
    def applyBonus(self,score,bonus):
        for key, value in bonus.items():
            while value > 0:
                score *= key
                value -= 1
        return score


    def placeWord(self,word,position,across=True):
        word = word.upper()
        # Place word on board
        if across:
            assert position[1] + len(word) - 1 <= 14, "'{}' does not fit on board".format(word)
        else:
            assert position[0] + len(word) - 1 <= 14, "'{}' does not fit on board".format(word)
        assert self.checkWordPlacement(word,position,across=across), "'{}' cannot be placed on board".format(word)

        score = 0
        bonus = {2:0,3:0}

        if across:
            for x, i in enumerate(range(position[1], position[1] + len(word))):
                self.board[position[0],i] = word[x]
                score, bonus = self.tabulateScore(word[x],score,(position[0],i),bonus)
                self.activeTiles[(position[0], i)] = word[x]

            score = self.applyBonus(score, bonus)
                
        else:
            for x, j in enumerate(range(position[0], position[0] + len(word))):
                self.board[j,position[1]] = word[x]
                score, bonus = self.tabulateScore(word[x], score, (j, position[1]), bonus)
                self.activeTiles[(j, position[1])] = word[x]
            
            score = self.applyBonus(score, bonus)
        
        return score
    

if __name__ == "__main__":
    b = Board()
    print(b.placeWord('here',(7,6)))
    print(b.placeWord('here',(8,5)))
    print(b.placeWord('her',(9,4)))
    print(b.placeWord('house',(9,4),across=False))
    print(b.placeWord('heres',(7,6)))
    print(b.placeWord('said',(14,4)))
    b.showBoard()















#
