import sys
import re
from xmlrpc.client import MAXINT

class Board:
    config = {}
    placeable = {}
    rows = 0
    cols = 0

    def __init__(self):
        self.config = {}
        self.placeable = {}
        self.rows = 0
        self.cols = 0

    def makeBoard(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.config[(i, j)] = "E"
                self.placeable[(i, j)] = MAXINT

    def getPos(self, state, piece): # Gets all placeable positions
        i = 0
        for key in self.placeable.keys():
            posX = key[0]
            posY = key[1]

            # Get the moves of the current piece
            if piece.name == "King":
                moves, count = self.movesKing(state, posX, posY, True)
                value = len(moves) - count - 1 
            if piece.name == "Rook":
                moves, count = self.movesRook(state, posX, posY, True)
                value = len(moves) - count - 1 
            if piece.name == "Bishop":
                moves, count = self.movesBishop(state, posX, posY, True)
                value = len(moves) - count - 1 
            if piece.name == "Queen":
                moves, count = self.movesQueen(state, posX, posY, True)
                value = len(moves) - count - 1 
            if piece.name == "Knight":
                moves, count = self.movesKnight(state, posX, posY, True)
                value = len(moves) - count - 1 

            self.placeable[key] = value
            i += 1
            if i == 10:
                break
            
        sortedPos = {k: v for k, v in sorted(self.placeable.items(), key=lambda item: -item[1])} 
        return sortedPos   

    def assign(self, state, piece, pos):
        posX = pos[0]
        posY = pos[1]
        
        # Get the moves of the current piece
        if piece.name == "King":
            self.config[pos] = "K"
            state.numOfKing -= 1
            moves = self.movesKing(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Rook":
            self.config[pos] = "R"
            state.numOfRook -= 1
            moves = self.movesRook(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Bishop":
            self.config[pos] = "B"
            state.numOfBishop -= 1
            moves = self.movesBishop(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Queen":
            self.config[pos] = "Q"
            state.numOfQueen -= 1
            moves = self.movesQueen(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Knight":
            self.config[pos] = "N"
            state.numOfKnight -= 1
            moves = self.movesKnight(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos

        state.assignment[pos] = piece
        del self.placeable[pos]

        for move in moves: # Change the placeable dict
            mposX = move[0]
            mposY = move[1]
            mPos = (mposX, mposY)
            # adds the pos piece attacks
            state.assignment[pos].attacks.append(mPos)
            if mPos in self.placeable.keys():
                del self.placeable[mPos]

    def removePiece(self, state, piece, pos):
        posX = pos[0]
        posY = pos[1]

        # Get the moves of the current piece
        if piece.name == "King":
            state.numOfKing += 1
            moves = self.movesKing(state, posX, posY, False)
            # moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Rook":
            state.numOfRook += 1
            moves = self.movesRook(state, posX, posY, False)
            # moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Bishop":
            state.numOfBishop += 1
            moves = self.movesBishop(state, posX, posY, False)
            # moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Queen":
            state.numOfQueen += 1
            moves = self.movesQueen(state, posX, posY, False)
            # moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Knight":
            state.numOfKnight += 1
            moves = self.movesKnight(state, posX, posY, False)
            # moves.remove([posX, posY]) # Removes self pos

        del state.assignment[pos] # Removes the assignment
        self.config[pos] = "E"

        # Repopulate placeable dict
        for move in moves:
            mposX = move[0]
            mposY = move[1]
            mPos = (mposX, mposY)
            # check if really no other ones
            for key in state.assignment.keys():
                if not(mPos in state.assignment[key].attacks):
                    self.placeable[mPos] = MAXINT

    def isConsistent(self, state, piece, pos):
        posX = pos[0]
        posY = pos[1]

        # Get the moves of the current piece
        if piece.name == "King":
            moves = self.movesKing(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Rook":
            moves = self.movesRook(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Bishop":
            moves = self.movesBishop(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Queen":
            moves = self.movesQueen(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos
        if piece.name == "Knight":
            moves = self.movesKnight(state, posX, posY, False)
            moves.remove([posX, posY]) # Removes self pos

        for move in moves:
            mPosX = move[0]
            mposY = move[1]
            mPos = (mPosX, mposY)
            if mPos in state.assignment.keys():
                return False
        return True

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

    def setObstacles(self, state, positions):
        positions = positions.split()
        for position in positions:
            # print(position)
            numPos = self.toNumPos(position)
            state.obstacles[(numPos[0], numPos[1])] = "Obstacle"
            del self.placeable[(numPos[0], numPos[1])]

    def isInBoard(self, posX, posY):
        return posX >= 0 and posX < self.rows and posY >= 0 and posY < self.cols

    def isBlockedByObstacle(self, state, posX, posY):
        # aPosX = self.toAlphaPos(posX)
        alphaPos = (posX, posY)
        return alphaPos in state.obstacles.keys()

    def isBlocked(self, state, posX, posY): # By enemy or obstacle
        aPosX = self.toAlphaPos(posX)
        alphaPos = (aPosX, posY)
        return alphaPos in state.pieces.keys() or alphaPos in state.obstacles.keys()

    def movesKing(self, state, posX, posY, getCount): # Includes the self position
        counter = 0
        moves = []
        # numPos = self.toNumPos(position)
        posX = posX - 1
        posY = posY - 1
        for i in range(0, 3):
            for j in range(0, 3):
                newX = posX + i
                newY = posY + j
                anewX = self.toAlphaPos(newX)
                if self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                    moves.append([newX, newY])
                    if not((anewX, newY) in self.placeable.keys()):
                        counter += 1
        if getCount:
            return moves, counter
        else:
            return moves

    def movesRook(self, state, posX, posY, getCount): # Includes the self position
        counter = 0
        moves = []
        # numPos = self.toNumPos(position)
        # posX = int(numPos[0])
        # posY = int(numPos[1])

        ## Moving "Up" ->
        for i in range(1, self.rows):
            newX = posX
            newY = posY + i
            if not(self.isInBoard(newX, newY)):
                break

            if self.isBlockedByObstacle(state, newX, newY):
                break
            
            if self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                moves.append([newX, newY])
                anewX = self.toAlphaPos(newX)
                if not((anewX, newY) in self.placeable.keys()):
                    counter += 1
        
        ## Moving "Down" <-
        for i in range(1, self.rows):
            newX = posX
            newY = posY - i
            if not(self.isInBoard(posX, newY)):
                break
            
            if self.isBlockedByObstacle(state, posX, newY):
                break

            if self.isInBoard(posX, newY) and not(self.isBlockedByObstacle(state, posX, newY)):
                moves.append([posX, newY])
                anewX = self.toAlphaPos(posX)
                if not((anewX, newY) in self.placeable.keys()):
                    counter += 1
        
        ## Moving "Left" v
        for i in range(1, self.cols):
            newX = posX - i
            newY = posY
            if not(self.isInBoard(newX, posY)):
                break

            if self.isBlockedByObstacle(state, newX, posY):
                break

            if self.isInBoard(newX, posY) and not(self.isBlockedByObstacle(state, newX, posY)):
                moves.append([newX, posY])
                anewX = self.toAlphaPos(newX)
                newY = posY
                if not((anewX, newY) in self.placeable.keys()):
                    counter += 1
        
        ## Moving "Right" ^
        for i in range(1, self.cols):
            newX = posX + i
            newY = posY
            if not(self.isInBoard(newX, posY)):
                break

            if self.isBlockedByObstacle(state, newX, posY):
                break

            if self.isInBoard(newX, posY) and not(self.isBlockedByObstacle(state, newX, posY)):
                moves.append([newX, posY])
                anewX = self.toAlphaPos(newX)
                newY = posY
                if not((anewX, newY) in self.placeable.keys()):
                    counter += 1

        moves.append([posX, posY])
        if getCount:
            return moves, counter
        else:
            return moves

    def movesBishop(self, state, posX, posY, getCount): # Includes the self position
        counter = 0
        moves = []
        # numPos = self.toNumPos(position)
        # posX = int(numPos[0])
        # posY = int(numPos[1])

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
                        anewX = self.toAlphaPos(newX)
                        if not((anewX, newY) in self.placeable.keys()):
                            counter += 1

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
                        anewX = self.toAlphaPos(newX)
                        if not((anewX, newY) in self.placeable.keys()):
                            counter += 1

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
                        anewX = self.toAlphaPos(newX)
                        if not((anewX, newY) in self.placeable.keys()):
                            counter += 1

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
                        anewX = self.toAlphaPos(newX)
                        if not((anewX, newY) in self.placeable.keys()):
                            counter += 1
        
        moves.append([posX, posY])
        if getCount:
            return moves, counter
        else:
            return moves

    def movesQueen(self, state, posX, posY, getCount): # Includes the self position
        counter = 0
        movesR, countR = self.movesRook(state, posX, posY, True)
        movesB, countB = self.movesBishop(state, posX, posY, True)
        moves = movesR + movesB
        counter = countR + countB
        moves.remove([posX, posY])
        if getCount:
            return moves, counter
        else:
            return moves

    def movesKnight(self, state, posX, posY, getCount): # Includes the self position
        counter = 0
        moves = []
        dx = [-2, -1, 1, 2, -2, -1, 1, 2]
        dy = [-1, -2, -2, -1, 1, 2, 2, 1]
        # numPos = self.toNumPos(position)
        # posX = int(numPos[0])
        # posY = int(numPos[1])

        for i in range(8):
            newX = posX + dx[i]
            newY = posY + dy[i]
            if self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(state, newX, newY)):
                moves.append([newX, newY])
                anewX = self.toAlphaPos(newX)
                if not((anewX, newY) in self.placeable.keys()):
                    counter += 1
        moves.append([posX, posY])
        if getCount:
            return moves, counter
        else:
            return moves

class Piece:
    name = ""
    attacks = []

    def __init__(self, name):
        self.name = name
        self.attacks = []

class State:
    assignment = {}
    obstacles = {}
    numOfKing = 0
    numOfQueen = 0
    numOfBishop = 0
    numOfRook = 0
    numOfKnight = 0

    def __init__(self, obstacles, numOfKing, numOfQueen, numOfBishop, numOfRook, numOfKnight):
        self.assignment = {}
        self.obstacles = obstacles
        self.numOfKing = numOfKing
        self.numOfQueen = numOfQueen
        self.numOfBishop = numOfBishop
        self.numOfRook = numOfRook
        self.numOfKnight = numOfKnight

    def totalPieces(self):
        return self.numOfKing + self.numOfBishop + self.numOfKnight + self.numOfQueen + self.numOfRook

    def toPlace(self):
        if self.numOfQueen > 0:
            return Piece("Queen")
        if self.numOfRook > 0:
            return Piece("Rook")
        if self.numOfBishop > 0:
            return Piece("Bishop")
        if self.numOfKnight > 0:
            return Piece("Knight")
        if self.numOfKing > 0:
            return Piece("King")

def search(board, state):
    return backtrack(board, state)

def backtrack(board, state):
    if state.totalPieces() == 0:
        return state.assignment
    pieceToPlace = state.toPlace()
    sortedPos = board.getPos(state, pieceToPlace)
    for pos in sortedPos:
        if board.isConsistent(state, pieceToPlace, pos):
            board.assign(state, pieceToPlace, pos)
            if len(board.placeable.keys()) >= state.totalPieces():
                result = backtrack(board, state)
                if result != False:
                    return result
            board.removePiece(state, pieceToPlace, pos)
    return False

def parseResult(board, goalState):
    goal = {}
    for key in goalState.keys():
        keyX = board.toAlphaPos(key[0])
        keyY = key[1]
        Key = (keyX, keyY)
        goal[Key] = goalState[key].name
    return goal
### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    # You can code in here but you cannot remove this function or change the return type
    testfile = sys.argv[1] #Do not remove. This is your input testfile.
    board = Board()
    state = State({}, 0, 0, 0, 0, 0)
    parseInputFile(board, state, testfile)
    goalState = search(board, state)
    return parseResult(board, goalState) #Format to be returned

def parseInputFile(board, state, inFile):
    with open(inFile,'r') as inputFile:
        lines = inputFile.read().splitlines()
        for i in range(0, len(lines)):
            parsedLine = lines[i].partition(":")

            ## Constructs the board when row and col is available and board is empty
            if (board.rows != 0) & (board.cols != 0) & (board.config == {}):
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

            # Gets the number of each pieces
            if "number of king," in parsedLine[0].lower():
                numOfPieces = parsedLine[2].split(" ")
                state.numOfKing = int(numOfPieces[0])
                state.numOfQueen = int(numOfPieces[1])
                state.numOfBishop = int(numOfPieces[2])
                state.numOfRook = int(numOfPieces[3])
                state.numOfKnight = int(numOfPieces[4])
                
run_CSP()