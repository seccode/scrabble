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
        self.blanksMap = {}

    def pickTile(self):
        # Randomly pick tile and remove from tile set
        ret = self.tiles.pop()
        self.tileCount[ret] -= 1
        self.tilesLeft -= 1
        return ret

    def showBoard(self,tiles=[],scores=[]):
        plt.close()
        plt.ion()
        plt.show()
        fig, ax = plt.subplots(1,figsize=(8,8))
        plt.axis("off")
        ax.set_xlim(-35,self.size*10 + 45)
        ax.set_ylim(-55,self.size*10 + 15)
        plt.gca().set_aspect('equal', adjustable='box')

        if len(tiles) > 0:
            for i in range(len(tiles)):
                for j in range(len(tiles[i])):
                    rect = Rectangle((j*15 - 35 + (i%2!=0)*(115),- 20 - (30)*(i>1)),15,15,
                                    linewidth=1,edgecolor='k',facecolor='peru')
                    ax.add_patch(rect)
                    ax.annotate("Player {}, Score: {} ".format(i + 1, int(scores[i])), (17.5 + (i % 2 != 0)*(115), - (30)*(i > 1)),
                                color='black', weight='bold', fontsize=12, ha='center', va='center')
                    ax.annotate(tiles[i][j], (j*15 - 28 + (i % 2 != 0)*(115), - 13 - (30)*(i > 1)), color='white',
                                weight='bold', fontsize=18, ha='center', va='center')
                    ax.annotate(self.tileScores[tiles[i][j]], (j*15 - 23 + (i % 2 != 0)*(115), - 17.5 - (30)*(i>1)), color='white',
                                weight='bold', fontsize=8, ha='center', va='center')


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
                x_shift = 0
                y_shift = 0
                if self.board[i,j] != '':
                    tileColor = 'peru'
                    text = self.board[i,j].upper()
                    color = 'white'
                    subtext = self.tileScores[text]
                    if text == ' ':
                        text = self.blanksMap[(i,j)]
                        color = 'red'
                    weight = 14
                    x_shift = -1
                    y_shift = -0.5
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

                ax.annotate(text, (j*10 + 5 + x_shift, self.size*10 - i*10 + 5 + y_shift), color=color,
                            weight='bold', fontsize=weight, ha='center', va='center')
                ax.annotate(subtext, (j*10 + 8, self.size*10 - i*10 + 2), color='white',
                            weight='bold', fontsize=6, ha='center', va='center')

        # Add star at middle
        if (7,7) not in self.activeTiles:
            ax.scatter(75,85,marker='*',s=400,c='k',zorder=100)
        
        while True:
            plt.pause(10)

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
            return word, t
        else:
            l, r = position[1], position[1]
            while l > 0:
                if self.board[position[0],l-1] != '':
                    l -= 1
                else:
                    break
            while r < self.board.shape[1] - 1:
                if self.board[position[0],r+1] != '':
                    r += 1
                else:
                    break
            word = ''.join(self.board[position[0], l:position[1]]) + letter + ''.join(self.board[position[0], r+1:position[1]])
            return word, l

    def checkValidWord(self,word):
        # Check if a word is in official scrabble dictionary
        return word.upper() in self.validWords
    
    def getAdjacentWords(self,word,position,across=True):
        # Return dictionary of words formed by placement of main word, key is start position
        words = {}
        if across:
            for x, i in enumerate(range(position[1], position[1] + len(word))):
                if (position[0],i) in self.activeTiles:
                    continue
                res, start = self.expandPosition(word[x], (position[0], i), across=True)
                if len(res) > 1:
                    words[(start,i)] = res
        else:
            for x, j in enumerate(range(position[0], position[0] + len(word))):
                if (j, position[1]) in self.activeTiles:
                    continue
                res, start = self.expandPosition(word[x], (j, position[1]), across=False)
                if len(res) > 1:
                    words[(j,start)] = res
        return words

    def checkWordPlacement(self,word,position,across=True):
        # Check if given word can be placed on board in given position
        assert self.checkValidWord(word), "'{}' is not a valid word".format(word)

        # Check validity of all words that are created by touching this word
        words = self.getAdjacentWords(word,position,across=across)
        
        return all([self.checkValidWord(x) for x in words.values()])
    
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

    def scoreWord(self,word,position,across=True,place=False,blanks={}):
        score = 0
        bonus = {2: 0, 3: 0}
        uniqueTiles = 0

        if across:
            for x, i in enumerate(range(position[1], position[1] + len(word))):
                if (position[0],i) in self.blanksMap:
                    _, bonus = self.tabulateScore(word[x],score,(position[0],i),bonus)    
                    if place:
                        if (position[0], i) not in self.activeTiles:
                            uniqueTiles += 1
                        self.board[position[0], i] = ' '
                        self.activeTiles[(position[0], i)] = ' '
                    continue

                score, bonus = self.tabulateScore(word[x],score,(position[0],i),bonus)
                if place:
                    if (position[0],i) not in self.activeTiles:
                        uniqueTiles += 1
                    self.board[position[0], i] = word[x]
                    self.activeTiles[(position[0], i)] = word[x]
                    

            score = self.applyBonus(score, bonus)
                
        else:
            for x, j in enumerate(range(position[0], position[0] + len(word))):
                if (j,position[1]) in self.blanksMap:
                    _, bonus = self.tabulateScore(word[x],score,(j,position[1]), bonus)
                    if place:
                        if (j,position[1]) not in self.activeTiles:
                            uniqueTiles += 1
                        self.board[j, position[1]] = ' '
                        self.activeTiles[(j, position[1])] = ' '
                    continue

                score, bonus = self.tabulateScore(word[x], score, (j, position[1]), bonus)
                if place:
                    if (j, position[1]) not in self.activeTiles:
                        uniqueTiles += 1
                    self.board[j,position[1]] = word[x]
                    self.activeTiles[(j, position[1])] = word[x]
            
            score = self.applyBonus(score, bonus)
        
        return score + (uniqueTiles == 7)*50

    def checkAnchoring(self,word,position,across=True):
        # Ensure word placement is valid
        anchored = False

        if len(self.activeTiles) == 0:
            if across and ((7,7) in [(position[0],j) for j in range(position[1],position[1]+len(word))]):
                anchored = True
            elif not across and ((7,7) in [(i,position[1]) for i in range(position[0],position[0]+len(word))]):
                anchored = True
        elif across:
            if any([(letter != '') for letter in self.board[position[0],position[1]:position[1]+len(word)]]) or (len(self.getAdjacentWords(word,position,across=True)) != 0):
                if not ((position[1] - 1 >= 0 and self.board[position[0],position[1]-1] != '') or \
                        (position[1] + len(word) <= self.size and self.board[position[0],position[1]+len(word)] != '')):
                    anchored = True
        else:
            if any([(letter != '') for letter in self.board[position[0]:position[0]+len(word),position[1]]]) or (len(self.getAdjacentWords(word,position,across=False)) != 0):
                if not ((position[0] - 1 >= 0 and self.board[position[0]-1,position[1]] != '') or \
                        (position[0] + len(word) <= self.size and self.board[position[0]+len(word),position[1]] != '')):
                    anchored = True

        return anchored

    def findScore(self,word,position,across=True,place=False,blanks={}):
        word = word.upper()
        # Use this function to determine the score for this move, use place=False to 
        # find score but not place move on board
        score = 0
        adjWords = self.getAdjacentWords(word, position, across=across)
        for pos, subWord in adjWords.items():
            score += self.scoreWord(subWord, pos, across=not across)

        return score + self.scoreWord(word, position, across=across, place=place, blanks=blanks)

    def placeWord(self,word,position,across=True,blanks={}):
        word = word.upper()
        # Place word on board
        assert self.checkAnchoring(word,position,across=across), "Word is not anchored properly"

        if across:
            assert position[1] + len(word) - 1 <= 14, "'{}' does not fit on board".format(word)
        else:
            assert position[0] + len(word) - 1 <= 14, "'{}' does not fit on board".format(word)
        assert self.checkWordPlacement(word,position,across=across), "'{}' cannot be placed on board".format(word)

        for k, v in blanks.items():
            self.blanksMap[k] = v
            
        return self.findScore(word,position,across=across,place=True,blanks=blanks)

if __name__ == "__main__":
    b = Board()
    print(b.placeWord('here',(7,6)))
    print(b.placeWord('here',(8,5)))
    print(b.placeWord('her',(9,4)))
    print(b.placeWord('house',(9,4),across=False))
    print(b.placeWord('heres',(7,6)))
    print(b.findScore('said',(14,4)))
    b.showBoard()















#
