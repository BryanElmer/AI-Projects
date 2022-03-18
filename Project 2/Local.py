import sys
import re
import random
from xmlrpc.client import MAXINT
import copy
random.seed(1)

class Board:
    config = []
    rows = 0
    cols = 0
    K = 0

    def __init__(self):
        self.config = []
        self.rows = 0
        self.cols = 0
        self.K = MAXINT

    def makeBoard(self):
        for i in range(self.rows):
            self.config.append([])
            for j in range(self.cols):
                self.config[-1].append(0)

    def toNumPos(self, pos):
        charDict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,"k": 10, "l": 11, "m": 12, "n": 13, 
        "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
        posList = re.split('(\d+)', pos)
        return [int(charDict[posList[0]]), int(posList[1])]

    def toSingleNumPos(self, pos):
        charDict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,"k": 10, "l": 11, "m": 12, "n": 13, 
        "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
        return int(charDict[pos])

    def toAlphaPos(self, pos):
        charList = list("abcdefghijklmnopqrstuvwxyz")
        return charList[pos]

    def getNumOfPieces(self, state):
        counter = 0
        for key in state.pieces.keys():
            if state.pieces[key] != "Obstacle":
                counter += 1
        return counter

    def calculateValue(self, state):
        for key in state.pieces.keys():
            currentPiece = state.pieces[key]
            posX = self.toSingleNumPos(key[0])
            posY = key[1]
            position = key[0] + str(key[1])

            # Get the moves of the current piece
            if currentPiece.name == "King":
                moves = self.movesKing(state, position)
                moves.remove([posX, posY]) # Removes self pos
            if currentPiece.name == "Rook":
                moves = self.movesRook(state, position)
                moves.remove([posX, posY]) # Removes self pos
            if currentPiece.name == "Bishop":
                moves = self.movesBishop(state, position)
                moves.remove([posX, posY]) # Removes self pos
            if currentPiece.name == "Queen":
                moves = self.movesQueen(state, position)
                moves.remove([posX, posY]) # Removes self posl
            if currentPiece.name == "Knight":
                moves = self.movesKnight(state, position)
                moves.remove([posX, posY]) # Removes self pos

            # Checks each moves of the current piece +1 to config if threaten
            for move in moves:
                mposX = move[0]
                mposY = move[1]
                maPosX = self.toAlphaPos(mposX)
                position = (maPosX, mposY)
                if position in state.pieces.keys():
                    self.config[posX][posY] += 1

    def resetValue(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.config[i][j] = 0

    def getValue(self, state):
        self.resetValue()
        self.calculateValue(state)
        value = 0
        for i in range(self.rows):
            for j in range(self.cols):
                value += self.config[i][j]
        # self.printBoard()
        return value

    def initializeAttacks(self, state):
        for key in state.pieces.keys(): # For all chess pieces
            currentPiece = state.pieces[key]
            posX = self.toSingleNumPos(key[0])
            posY = key[1]
            position = key[0] + str(key[1])

            # Get the moves of the current piece
            if currentPiece.name == "King":
                moves = self.movesKing(state, position)
                moves.remove([posX, posY]) # Removes self pos
            if currentPiece.name == "Rook":
                moves = self.movesRook(state, position)
                moves.remove([posX, posY]) # Removes self pos
            if currentPiece.name == "Bishop":
                moves = self.movesBishop(state, position)
                moves.remove([posX, posY]) # Removes self pos
            if currentPiece.name == "Queen":
                moves = self.movesQueen(state, position)
                moves.remove([posX, posY]) # Removes self pos
            if currentPiece.name == "Knight":
                moves = self.movesKnight(state, position)
                moves.remove([posX, posY]) # Removes self pos

            for move in moves:
                mposX = move[0]
                mposY = move[1]
                maPosX = self.toAlphaPos(mposX)
                mposition = (maPosX, mposY) # Position of enemy piece ?
                if mposition in state.pieces.keys():
                    currentPiece.attacks.append(mposition)
                    state.pieces[mposition].attackedBy.append(key)

    def getNeighbour(self, state): 
        values = {}
        for key in state.pieces.keys():
            testPieces = copy.deepcopy(state.getPieces())
            del testPieces[key]
            next = State(testPieces, state.getObstacles())
            value = self.getValue(next)
            values[key] = value

        minKeys = [key for key, value in values.items() if value == 
        min(values.values())]
        # print(values)
        # print(minKeys)

        # self.resetValue()
        # self.calculateValue(state)
        # self.printBoard()
        # maxValue = 0
        # positions = []
        # for i in range(self.rows):
        #     for j in range(self.cols):
        #         if maxValue == self.config[i][j]:
        #             positions.append([i, j])
        #         if maxValue < self.config[i][j]:
        #             maxValue = self.config[i][j]
        #             positions = [[i, j]]

        # print(positions)
        # Randomizer Element
        minKey = random.choice(minKeys)
        # print(minKey)
        # print(position)

        # aPosX = self.toAlphaPos(maxKey[0])
        # aPos = (aPosX, maxKey[1])
        pieces = state.getPieces()
        del pieces[minKey]
        neighbour = State(pieces, state.getObstacles())

        return neighbour

    def setObstacles(self, state, positions):
        positions = positions.split()
        for position in positions:
            numPos = self.toNumPos(position)
            posX = int(numPos[0])
            aPosX = self.toAlphaPos(posX)
            posY = int(numPos[1])
            state.obstacles[(aPosX, posY)] = "Obstacle"

    def setEnemy(self, state, piece, position):
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        aPosX = self.toAlphaPos(posX)
        posY = int(numPos[1])
        if piece.lower() == "king":
            state.pieces[(aPosX, posY)] = Piece("King")
        if piece.lower() == "rook":
            state.pieces[(aPosX, posY)] = Piece("Rook")
        if piece.lower() == "bishop":
            state.pieces[(aPosX, posY)] = Piece("Bishop")
        if piece.lower() == "queen":
            state.pieces[(aPosX, posY)] = Piece("Queen")
        if piece.lower() == "knight":
            state.pieces[(aPosX, posY)] = Piece("Knight")

    def isInBoard(self, posX, posY):
        return posX >= 0 and posX < self.rows and posY >= 0 and posY < self.cols

    def isBlockedByObstacle(self, state, posX, posY):
        aPosX = self.toAlphaPos(posX)
        alphaPos = (aPosX, posY)
        return alphaPos in state.obstacles.keys()

    def isBlocked(self, state, posX, posY): # By enemy or obstacle
        aPosX = self.toAlphaPos(posX)
        alphaPos = (aPosX, posY)
        return alphaPos in state.pieces.keys() or alphaPos in state.obstacles.keys()

    def movesKing(self, state, position): # Includes the self position
        moves = []
        numPos = self.toNumPos(position)
        posX = int(numPos[0]) - 1
        posY = int(numPos[1]) - 1
        for i in range(0, 3):
            for j in range(0, 3):
                newX = posX + i
                newY = posY + j
                if self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                    moves.append([newX, newY])
        return moves

    def movesRook(self, state, position): # Includes the self position
        moves = []
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1])

        ## Moving "Up" ->
        for i in range(1, self.rows):
            if not(self.isInBoard(posX, posY + i)):
                break

            if self.isBlockedByObstacle(state, posX, posY + i):
                break
            
            if self.isInBoard(posX, posY + i) and not(self.isBlockedByObstacle(state, posX, posY + i)):
               moves.append([posX, posY + i])
        
        ## Moving "Down" <-
        for i in range(1, self.rows):
            if not(self.isInBoard(posX, posY - i)):
                break
            
            if self.isBlockedByObstacle(state, posX, posY - i):
                break

            if self.isInBoard(posX, posY - i) and not(self.isBlockedByObstacle(state, posX, posY - i)):
               moves.append([posX, posY - i])
        
        ## Moving "Left" v
        for i in range(1, self.cols):
            if not(self.isInBoard(posX - i, posY)):
                break

            if self.isBlockedByObstacle(state, posX - i, posY):
                break

            if self.isInBoard(posX - i, posY) and not(self.isBlockedByObstacle(state, posX - i, posY)):
                moves.append([posX - i, posY])
        
        ## Moving "Right" ^
        for i in range(1, self.cols):
            if not(self.isInBoard(posX + i, posY)):
                break

            if self.isBlockedByObstacle(state, posX + i, posY):
                break

            if self.isInBoard(posX + i, posY) and not(self.isBlockedByObstacle(state, posX + i, posY)):
                moves.append([posX + i, posY])
        moves.append([posX, posY])
        return moves

    def movesBishop(self, state, position): # Includes the self position
        moves = []
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1])

        maxLimit = max(self.rows, self.cols)

        ## "top right"
        stop = False
        for i in range(1, maxLimit):
            for j in range(1, maxLimit):
                if i == j:
                    newX = posX + i
                    newY = posY + j
                    if not(self.isInBoard(newX, newY)):
                        stop = True
                        break

                    if self.isBlockedByObstacle(state, newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                        moves.append([newX, newY])

        ## "top left"
        stop = False
        for i in range(1, maxLimit):
            for j in range(1, maxLimit):
                if i == j:
                    newX = posX + i
                    newY = posY - j
                    if not(self.isInBoard(newX, newY)):
                        stop = True
                        break

                    if self.isBlockedByObstacle(state, newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                        moves.append([newX, newY])

        ## "bot right"
        stop = False
        for i in range(1, maxLimit):
            for j in range(1, maxLimit):
                if i == j:
                    newX = posX - i
                    newY = posY + j
                    if not(self.isInBoard(newX, newY)):
                        stop = True
                        break

                    if self.isBlockedByObstacle(state, newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                        moves.append([newX, newY])

        ## "bot left"
        stop = False
        for i in range(1, maxLimit):
            for j in range(1, maxLimit):
                if i == j:
                    newX = posX - i
                    newY = posY - j
                    if not(self.isInBoard(newX, newY)):
                        stop = True
                        break

                    if self.isBlockedByObstacle(state, newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                        moves.append([newX, newY])
        
        moves.append([posX, posY])
        return moves

    def movesQueen(self, state, position): # Includes the self position
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1]) 
        moves = self.movesRook(state, position) + self.movesBishop(state, position)
        moves.remove([posX, posY])
        return moves

    def movesKnight(self, state, position): # Includes the self position
        moves = []
        dx = [-2, -1, 1, 2, -2, -1, 1, 2]
        dy = [-1, -2, -2, -1, 1, 2, 2, 1]
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1])

        for i in range(8):
            newX = posX + dx[i]
            newY = posY + dy[i]
            if self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                moves.append([newX, newY])
        moves.append([posX, posY])
        return moves

    # def printBoard(self):
    #     for i in range(1, len(self.config) + 1):
    #         print("a", self.config[len(self.config) - i])

    #     print("    0, 1, 2, 3, ...")

    # def __str__(self):
    #     print("Rows:", self.rows)
    #     print("Cols:", end=" ")
    #     return str(self.cols)

class Piece:
    name = ""
    attacks = []
    attackedBy = []

    def __init__(self, name):
        self.name = name

    def printPiece(self):
        print("piece:", self.name)
        print("attacks:", self.attacks)
        print("attacked by:", end=" ")
        return str(self.attackedBy)
    pass

class State:
    pieces = {}
    obstacles = {}

    def __init__(self, pieces, obstacles):
        self.pieces = pieces
        self.obstacles = obstacles

    def getPieces(self):
        return self.pieces

    def getObstacles(self):
        return self.obstacles


def search(board, state):
    current = state
    board.initializeAttacks(current)
    for key in current.pieces.keys():
        current.pieces[key].printPiece()
    # while True:
    #     print("CURRENT:")
    #     print(current.getPieces())
    #     # print(board.getValue(current))
    #     # print('\n')
    #     neighbour = board.getNeighbour(current)
    #     # print("NEIGHBOUR:")
    #     # print(neighbour.getPieces())
    #     # print(board.getValue(neighbour))
    #     # print('\n')
    #     valueNeighbour = board.getValue(neighbour)
    #     # if len(neighbour.getPieces()) < board.K:
    #     #     return neighbour.pieces
    #     if valueNeighbour == 0 or valueNeighbour > board.getValue(current):
    #         return neighbour.pieces
    #     current = neighbour


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    # You can code in here but you cannot remove this function or change the return type
    testFile = sys.argv[1] #Do not remove. This is your input testfile.
    piecesLeft = 0
    board = Board()
    goalState = {}
    # i = 1
    while piecesLeft < board.K:
        # print("########## LOOP:", i, " ###########")
        state = State({}, {})
        parseInputFile(board, state, testFile)
        goalState = search(board, state)
        piecesLeft = len(goalState)
        # i += 1
    return goalState #Format to be returned

def parseInputFile(board, state, inFile):
    readPieces = False
    with open(inFile,'r') as inputFile:
        lines = inputFile.read().splitlines()
        for i in range(0, len(lines)):
            parsedLine = lines[i].partition(":")

            ## Constructs the board when row and col is available and board is empty
            if (board.rows != 0) & (board.cols != 0) & (board.config == []):
                board.makeBoard()

            ## Gets the num of rows and cols from the text file
            if parsedLine[0].lower() == "rows":
                board.cols = int(parsedLine[2])
            elif parsedLine[0].lower() == "cols":
                board.rows = int(parsedLine[2])

            ## Gets the num of obstacles and positions them into the board
            if "position of obstacles" in parsedLine[0].lower():
                if parsedLine[2] != "-":
                    board.setObstacles(state, parsedLine[2])

            ## Reads K (Minimum number of pieces left in goal)
            if "k (minimum number" in parsedLine[0].lower():
                board.K = int(parsedLine[2])
            
            if readPieces:
                enemy = parsedLine[0].replace("[", "").replace("]", "").split(",")
                board.setEnemy(state, enemy[0], enemy[1])

            ## Position of enemy pieces
            if "position of pieces" in parsedLine[0].lower():
                readPieces = True
                # print(i)
                # j = 1
                # parsedLine = lines[i+j].partition(":") # checks for next line
                # while i + j < len(lines): # TODO make sure this one correct looping
                #     enemy = parsedLine[0].replace("[", "").replace("]", "").split(",")
                #     board.setEnemy(state, enemy[0], enemy[1])
                #     j += 1
                #     parsedLine = lines[i+j].partition(":")

            
ans = run_local()
print(ans)
