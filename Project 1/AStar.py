import sys
import re

from queue import PriorityQueue

class Board:
    config = []
    rows = 0
    cols = 0
    numOfObstacles = 0

    def __init__(self):
        self.config = []
        self.rows = 0
        self.cols = 0

    def makeBoard(self):
        for i in range(self.rows):
            self.config.append([])
            for j in range(self.cols):
                self.config[-1].append(1)

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

    def setObstacles(self, positions):
        positions = positions.split()
        for position in positions:
            numPos = self.toNumPos(position)
            posX = int(numPos[0])
            posY = int(numPos[1])
            self.config[posX][posY] = -1 # set to -1 indicating obstacle, -2 blocked by enemy

    def setCost(self, position, cost):
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1])
        cost = int(cost)
        if self.config[posX][posY] > 0:
            self.config[posX][posY] = cost

    def setEnemy(self, piece, position):
        if piece.lower() == "king":
            blockPos = self.movesKing(position)
        if piece.lower() == "rook":
            blockPos = self.movesRook(position)
        if piece.lower() == "bishop":
            blockPos = self.movesBishop(position)
        if piece.lower() == "queen":
            blockPos = self.movesQueen(position)
        if piece.lower() == "knight":
            blockPos = self.movesKnight(position)

        for pos in blockPos:
            self.config[pos[0]][pos[1]] = -2        

    def isInBoard(self, posX, posY):
        return posX >= 0 and posX < self.rows and posY >= 0 and posY < self.cols

    def isBlockedByObstacle(self, posX, posY):
        return self.config[posX][posY] == -1

    def isBlocked(self, posX, posY): # By enemy or obstacle
        return self.config[posX][posY] < 0

    def movesKing(self, position): # Includes the self position
        moves = []
        numPos = self.toNumPos(position)
        posX = int(numPos[0]) - 1
        posY = int(numPos[1]) - 1
        for i in range(0, 3):
            for j in range(0, 3):
                newX = posX + i
                newY = posY + j
                if self.isInBoard(newX, newY) and not(self.isBlocked(newX, newY)):
                    moves.append([newX, newY])
        return moves

    def movesRook(self, position): # Includes the self position
        moves = []
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1])

        ## Moving "Up" ->
        for i in range(1, self.rows):
            if not(self.isInBoard(posX, posY + i)):
                break

            if self.isBlockedByObstacle(posX, posY + i):
                break
            
            if self.isInBoard(posX, posY + i) and not(self.isBlockedByObstacle(posX, posY + i)):
               moves.append([posX, posY + i])
        
        ## Moving "Down" <-
        for i in range(1, self.rows):
            if not(self.isInBoard(posX, posY - i)):
                break
            
            if self.isBlockedByObstacle(posX, posY - i):
                break

            if self.isInBoard(posX, posY - i) and not(self.isBlockedByObstacle(posX, posY - i)):
               moves.append([posX, posY - i])
        
        ## Moving "Left" v
        for i in range(1, self.cols):
            if not(self.isInBoard(posX - i, posY)):
                break

            if self.isBlockedByObstacle(posX - i, posY):
                break

            if self.isInBoard(posX - i, posY) and not(self.isBlockedByObstacle(posX - i, posY)):
                moves.append([posX - i, posY])
        
        ## Moving "Right" ^
        for i in range(1, self.cols):
            if not(self.isInBoard(posX + i, posY)):
                break

            if self.isBlockedByObstacle(posX + i, posY):
                break

            if self.isInBoard(posX + i, posY) and not(self.isBlockedByObstacle(posX + i, posY)):
                moves.append([posX + i, posY])
        moves.append([posX, posY])
        return moves

    def movesBishop(self, position): # Includes the self position
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

                    if self.isBlockedByObstacle(newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(newX, newY)):
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

                    if self.isBlockedByObstacle(newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(newX, newY)):
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

                    if self.isBlockedByObstacle(newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(newX, newY)):
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

                    if self.isBlockedByObstacle(newX, newY):
                        stop = True
                        break

                    if not(stop) and self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(newX, newY)):
                        moves.append([newX, newY])
        
        moves.append([posX, posY])
        return moves

    def movesQueen(self, position): # Includes the self position
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1]) 
        moves = self.movesRook(position) + self.movesBishop(position)
        moves.remove([posX, posY])
        return moves

    def movesKnight(self, position): # Includes the self position
        moves = []
        dx = [-2, -1, 1, 2, -2, -1, 1, 2]
        dy = [-1, -2, -2, -1, 1, 2, 2, 1]
        numPos = self.toNumPos(position)
        posX = int(numPos[0])
        posY = int(numPos[1])

        for i in range(8):
            newX = posX + dx[i]
            newY = posY + dy[i]
            if self.isInBoard(newX, newY) and not(self.isBlockedByObstacle(newX, newY)):
                moves.append([newX, newY])
        moves.append([posX, posY])
        return moves

    def printBoard(self):
        for i in range(1, len(self.config) + 1):
            print("a", self.config[len(self.config) - i])

        print("    0, 1, 2, 3, ...")

    def __str__(self):
        print("Rows:", self.rows)
        print("Cols:", self.cols)
        print("Number of obstacles:", end=" ")
        return str(self.numOfObstacles)

class State:
    posX = ""
    posY = ""
    goalX = []
    goalY = []
    moves = []
    pathCost = 0

    def __init__(self, posX, posY, goalX, goalY, moves, pathCost):
        self.posX = posX
        self.posY = posY
        self.goalX = goalX
        self.goalY = goalY
        self.moves = moves
        self.pathCost = pathCost

    def __lt__(self, other):
        return self.posX < other.posX or (self.posX == other.posX and int(self.posY) < int(other.posY))

    def isGoal(self):
        for i in range(len(self.goalX)):
            if (self.posX == self.goalX[i] and self.posY == self.goalY[i]):
                return True
        return False

    def h(self, board):
        numPosX = board.toSingleNumPos(self.posX)
        numPosY = int(self.posY)
        numGoalX = []
        numGoalY = []
        hList = []
        for i in self.goalX:
            numGoalX.append(board.toSingleNumPos(i))

        for j in self.goalY:
            numGoalY.append(int(j))

        for k in range(len(numGoalX)):
            hList.append(max(abs(numPosX - numGoalX[k]), abs(numPosY - numGoalY[k])))

        return min(hList)

    def __str__(self):
        print("Start X:", self.posX)
        print("Start Y:", self.posY)
        print("Goals X:", self.goalX)
        print("Goals Y:", end=" ")
        return str(self.goalY)

def search(board, state):
    frontier = PriorityQueue(maxsize = 0) # ["a", "1"]
    reached = {}
    nodesExplored = 0
    
    node = State(state.posX, state.posY, state.goalX, state.goalY, [], 0)
    frontier.put((node.pathCost + abs(node.h(board)), node))
    reached[state.posX + state.posY] = node

    while not(frontier.empty()):
        priority, currentNode = frontier.get()
        nodesExplored += 1

        if currentNode.isGoal():
            return currentNode.moves, nodesExplored, currentNode.pathCost

        numCurrentX = board.toSingleNumPos(currentNode.posX)
        numCurrentY = int(currentNode.posY)
        alphaCurrentPos = currentNode.posX + currentNode.posY
        actions = board.movesKing(alphaCurrentPos)
        actions.remove([numCurrentX, numCurrentY]) # Removes self pos

        for action in actions:
            alphaPosX = board.toAlphaPos(action[0])
            alphaPosY = str(action[1])
            alphaPos = alphaPosX + alphaPosY
            actionCost = int(board.config[action[0]][action[1]])
            newCost = currentNode.pathCost + actionCost
            actionNode = State(alphaPosX, alphaPosY, state.goalX, state.goalY, currentNode.moves + [[(currentNode.posX, int(currentNode.posY)), (alphaPosX, int(alphaPosY))]], newCost)
            if not(alphaPos in reached.keys()) or newCost < reached[alphaPos].pathCost: # check if action is not in reached, or cheaper path, then add to frontier
                # Add into reached set, with corresponding path cost (current cost + new action cost)
                reached[alphaPos] = actionNode
                frontier.put((actionNode.pathCost + abs(actionNode.h(board)), actionNode))
        if frontier.empty():
            return node.moves, nodesExplored, 0


### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_AStar():
    # You can code in here but you cannot remove this function or change the return type
    board = Board()
    state = State("", "", [], [], [], 0)
    parseInputFile(board, state)
    moves, nodesExplored, pathCost= search(board, state) #For reference
    return moves, nodesExplored, pathCost #Format to be returned
    
def parseInputFile(board, state):
    inFile = sys.argv[1]
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
            if parsedLine[0].lower() == "number of obstacles":
                board.numOfObstacles = int(parsedLine[2])
            elif "position of obstacles" in parsedLine[0].lower():
                board.setObstacles(parsedLine[2])

            ## Reads the step costs and set them into the board accordingly
            if "step cost" in parsedLine[0].lower():
                j = 1
                parsedLine = lines[i+j].partition(":") # checks for next line
                while not("number of enemy" in parsedLine[0].lower()):
                    stepCost = parsedLine[0].replace("[", "").replace("]", "").split(",")
                    position = stepCost[0]
                    cost = stepCost[1]
                    board.setCost(position, cost)
                    j += 1
                    parsedLine = lines[i+j].partition(":")

            ## Position of enemy pieces
            if "position of enemy" in parsedLine[0].lower():
                j = 1
                parsedLine = lines[i+j].partition(":") # checks for next line
                while not("number of own" in parsedLine[0].lower()):
                    enemy = parsedLine[0].replace("[", "").replace("]", "").split(",")
                    board.setEnemy(enemy[0], enemy[1])
                    j += 1
                    parsedLine = lines[i+j].partition(":")

            ## Starting position
            if "starting position of pieces" in parsedLine[0].lower():
                parsedLine = lines[i+1].replace("[", "").replace("]", "").split(",")
                pos = re.split('(\d+)', parsedLine[1])
                state.posX = pos[0]
                state.posY = pos[1]

            if "goal positions" in parsedLine[0].lower():
                goals = parsedLine[2].split()
                for goal in goals:
                    goalPos = re.split('(\d+)', goal)
                    state.goalX.append(goalPos[0])
                    state.goalY.append(goalPos[1])
