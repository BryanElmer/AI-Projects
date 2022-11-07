from xmlrpc.client import MAXINT, MININT

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# Helper functions to aid in your implementation. Can edit/remove
class Game:
    pieces = {}
    enemy = {}
    moveMade = []

    rows = 5
    cols = 5

    def __init__(self, pieces, enemy, moveMade):
        self.pieces = pieces
        self.enemy = enemy
        self.moveMade = moveMade

    def getPieces(self):
        return self.pieces

    def getEnemy(self):
        return self.enemy

    def getTotalPieces(self):
        return len(self.pieces) + len(self.enemy)

    def toAlphaPos(self, pos):
        charList = list("abcde")
        return charList[pos]

    def toSingleNumPos(self, pos):
        charDict = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9,"k": 10, "l": 11, "m": 12, "n": 13, 
        "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24, "z": 25}
        return int(charDict[pos])

    def isInBoard(self, posX, posY):
        return posX >= 0 and posX < self.rows and posY >= 0 and posY < self.cols

    def isEnemyBlocked(self, posX, posY):
        key = (posX, posY)
        return key in self.enemy.keys()

    def isSelfBlocked(self, posX, posY):
        key = (posX, posY)
        return key in self.pieces.keys()

    def isBlocked(self, posX, posY):
        return self.isEnemyBlocked(posX, posY) or self.isSelfBlocked(posX, posY)
    
    def movesKing(self, posX, posY, isMaxPlayer): # Not include the self position
        moves = []
        posX = posX - 1
        posY = posY - 1
        for i in range(0, 3):
            for j in range(0, 3):
                newX = posX + i
                newY = posY + j
                if isMaxPlayer:
                    if self.isInBoard(newX, newY) and not(self.isSelfBlocked(newX, newY)):
                        moves.append([newX, newY])
                else:
                    if self.isInBoard(newX, newY) and not(self.isEnemyBlocked(newX, newY)):
                        moves.append([newX, newY])
        if [posX + 1, posY + 1] in moves:
            moves.remove([posX + 1, posY + 1])
        return moves
    
    def movesRook(self, posX, posY, isMaxPlayer): # Not include the self position
        moves = []

        ## Moving "Up" ->
        for i in range(1, self.rows):
            newX = posX
            newY = posY + i

            if not(self.isInBoard(newX, newY)):
                break
                
            if isMaxPlayer:
                if self.isSelfBlocked(newX, newY):
                    break

                if self.isEnemyBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isSelfBlocked(newX, newY)):
                    moves.append([newX, newY])
            else: 
                if self.isEnemyBlocked(newX, newY):
                    break

                if self.isSelfBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isEnemyBlocked(newX, newY)):
                    moves.append([newX, newY])
        
        ## Moving "Down" <-
        for i in range(1, self.rows):
            newX = posX
            newY = posY - i

            if not(self.isInBoard(newX, newY)):
                break
                
            if isMaxPlayer:
                if self.isSelfBlocked(newX, newY):
                    break

                if self.isEnemyBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isSelfBlocked(newX, newY)):
                    moves.append([newX, newY])
            else: 
                if self.isEnemyBlocked(newX, newY):
                    break

                if self.isSelfBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isEnemyBlocked(newX, newY)):
                    moves.append([newX, newY])
        
        ## Moving "Left" v
        for i in range(1, self.cols):
            newX = posX - i
            newY = posY
            if not(self.isInBoard(newX, newY)):
                break
                
            if isMaxPlayer:
                if self.isSelfBlocked(newX, newY):
                    break

                if self.isEnemyBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isSelfBlocked(newX, newY)):
                    moves.append([newX, newY])
            else: 
                if self.isEnemyBlocked(newX, newY):
                    break

                if self.isSelfBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isEnemyBlocked(newX, newY)):
                    moves.append([newX, newY])

        
        ## Moving "Right" ^
        for i in range(1, self.cols):
            newX = posX + i
            newY = posY
            if not(self.isInBoard(newX, newY)):
                break
                
            if isMaxPlayer:
                if self.isSelfBlocked(newX, newY):
                    break

                if self.isEnemyBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isSelfBlocked(newX, newY)):
                    moves.append([newX, newY])
            else: 
                if self.isEnemyBlocked(newX, newY):
                    break

                if self.isSelfBlocked(newX, newY):
                    moves.append([newX, newY])
                    break
                
                if self.isInBoard(newX, newY) and not(self.isEnemyBlocked(newX, newY)):
                    moves.append([newX, newY])

        # moves.append([posX, posY])
        return moves

    def movesBishop(self, posX, posY, isMaxPlayer): # Not include the self position
        moves = []

        adder = [1, 2, 3, 4]
        for i in range(0, 4): # bot right
            newX = posX + adder[i]
            newY = posY + adder[i]
            if not(self.isInBoard(newX, newY)):
                break
            if isMaxPlayer and self.isSelfBlocked(newX, newY):
                break
            if isMaxPlayer and self.isEnemyBlocked(newX, newY):
                moves.append([newX, newY])
                break
            if not(isMaxPlayer) and self.isEnemyBlocked(newX, newY):
                break
            if not(isMaxPlayer) and self.isSelfBlocked(newX, newY):
                moves.append([newX, newY])
                break
            moves.append([newX, newY])
        
        for i in range(0, 4): # bot left
            newX = posX - adder[i]
            newY = posY + adder[i]
            if not(self.isInBoard(newX, newY)):
                break
            if isMaxPlayer and self.isSelfBlocked(newX, newY):
                break
            if isMaxPlayer and self.isEnemyBlocked(newX, newY):
                moves.append([newX, newY])
                break
            if not(isMaxPlayer) and self.isEnemyBlocked(newX, newY):
                break
            if not(isMaxPlayer) and self.isSelfBlocked(newX, newY):
                moves.append([newX, newY])
                break
            moves.append([newX, newY])

        for i in range(0, 4): # top left
            newX = posX - adder[i]
            newY = posY - adder[i]
            if not(self.isInBoard(newX, newY)):
                break
            if isMaxPlayer and self.isSelfBlocked(newX, newY):
                break
            if isMaxPlayer and self.isEnemyBlocked(newX, newY):
                moves.append([newX, newY])
                break
            if not(isMaxPlayer) and self.isEnemyBlocked(newX, newY):
                break
            if not(isMaxPlayer) and self.isSelfBlocked(newX, newY):
                moves.append([newX, newY])
                break
            moves.append([newX, newY])

        for i in range(0, 4): # top right
            newX = posX + adder[i]
            newY = posY - adder[i]
            if not(self.isInBoard(newX, newY)):
                break
            if isMaxPlayer and self.isSelfBlocked(newX, newY):
                break
            if isMaxPlayer and self.isEnemyBlocked(newX, newY):
                moves.append([newX, newY])
                break
            if not(isMaxPlayer) and self.isEnemyBlocked(newX, newY):
                break
            if not(isMaxPlayer) and self.isSelfBlocked(newX, newY):
                moves.append([newX, newY])
                break
            moves.append([newX, newY])

        return moves

    def movesQueen(self, posX, posY, isMaxPlayer): # Not include the self position
        movesR = self.movesRook(posX, posY, isMaxPlayer)
        movesB = self.movesBishop(posX, posY, isMaxPlayer)
        moves = movesR + movesB
        # moves.remove([posX, posY])
        # moves.remove([posX, posY])
        return moves

    def movesKnight(self, posX, posY, isMaxPlayer): # Not include the self position
        moves = []
        dx = [-2, -1, 1, 2, -2, -1, 1, 2]
        dy = [-1, -2, -2, -1, 1, 2, 2, 1]

        for i in range(8):
            newX = posX + dx[i]
            newY = posY + dy[i]
            if isMaxPlayer:
                if self.isInBoard(newX, newY) and not(self.isSelfBlocked(newX, newY)):
                    moves.append([newX, newY])
            else: 
                if self.isInBoard(newX, newY) and not(self.isEnemyBlocked(newX, newY)):
                    moves.append([newX, newY])
        # moves.append([posX, posY])
        return moves

    def movesPawn(self, posX, posY, isMaxPlayer): # Not include self position
        moves = []
        if isMaxPlayer:
            newX = posX 
            newY = posY + 1 # depends on the config of the board TODO
            
            if self.isInBoard(newX, newY) and not(self.isBlocked(newX, newY)):
                moves.append([newX, newY])
            
            newX = posX + 1
            if self.isInBoard(newX, newY) and self.isEnemyBlocked(newX, newY):
                moves.append([newX, newY])

            newX = posX - 1
            if self.isInBoard(newX, newY) and self.isEnemyBlocked(newX, newY):
                moves.append([newX, newY])
        else:
            newX = posX
            newY = posY - 1

            if self.isInBoard(newX, newY) and not(self.isBlocked(newX, newY)):
                moves.append([newX, newY])

            newX = posX + 1
            if self.isInBoard(newX, newY) and self.isSelfBlocked(newX, newY):
                moves.append([newX, newY])

            newX = posX - 1
            if self.isInBoard(newX, newY) and self.isSelfBlocked(newX, newY):
                moves.append([newX, newY])

        return moves

    def getSuccessor(self, isMaxPlayer):
        totalMoves = []
        moves = []
        if isMaxPlayer:
            for key in self.pieces.keys(): # for each of the pieces
                # posX = self.toSingleNumPos(key[0])
                posX = key[0]
                posY = key[1]

                if self.pieces[key] == 'King':
                    moves = self.movesKing(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Queen':
                    moves = self.movesQueen(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Bishop':
                    moves = self.movesBishop(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Knight':
                    moves = self.movesKnight(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Rook':
                    moves = self.movesRook(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Pawn':
                    moves = self.movesPawn(posX, posY, isMaxPlayer)
                
                for move in moves:
                    totalMoves.append([(posX, posY), (move[0], move[1])])
        else:
            for key in self.enemy.keys():
                # posX = self.toSingleNumPos(key[0])
                posX = key[0]
                posY = key[1]

                if self.enemy[key] == 'King':
                    moves = self.movesKing(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Queen':
                    moves = self.movesQueen(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Bishop':
                    moves = self.movesBishop(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Knight':
                    moves = self.movesKnight(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Rook':
                    moves = self.movesRook(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Pawn':
                    moves = self.movesPawn(posX, posY, isMaxPlayer)

                for move in moves: # [(1, 1), (1, 2)]
                    totalMoves.append([(posX, posY), (move[0], move[1])])
        
        return totalMoves

    def executeMove(self, move, isMaxPlayer):
        hasWon = MININT
        fromPos = move[0]
        toPos = move[1]
        newPieces = {**self.getPieces()}
        newEnemy = {**self.getEnemy()}
        newGame = Game(newPieces, newEnemy, [])
        
        if isMaxPlayer:
            piece = newGame.pieces[fromPos] # get name
            del newGame.pieces[fromPos] # del from old pos
            newGame.pieces[toPos] = piece # add to new pos
            if toPos in newGame.enemy.keys() and newGame.enemy[toPos] != 'King': # only can remove non kings
                del newGame.enemy[toPos]
            if toPos in newGame.enemy.keys() and newGame.enemy[toPos] == 'King': # captured the king
                del newGame.enemy[toPos]
                hasWon = 1
            if newGame.isCheck(True):
                hasWon = -500
        else:
            piece = newGame.enemy[fromPos]
            del newGame.enemy[fromPos]
            newGame.enemy[toPos] = piece
            if toPos in newGame.pieces.keys() and newGame.pieces[toPos] != 'King':
                del newGame.pieces[toPos]
            if toPos in newGame.pieces.keys() and newGame.pieces[toPos] == 'King':
                del newGame.enemy[toPos]
                hasWon = -1
            if newGame.isCheck(False):
                hasWon = -500
        
        newGame.moveMade = move
        return newGame, hasWon

    def getValue(self):
        totalWhite = 0
        totalBlack = 0
        for key in self.pieces.keys():
            if self.pieces[key] == 'King':
                totalWhite += 100
            if self.pieces[key] == 'Queen':
                totalWhite += 50
            if self.pieces[key] == 'Rook':
                totalWhite += 5
            if self.pieces[key] == 'Knight' or self.pieces[key] == 'Bishop':
                totalWhite += 3
            if self.pieces[key] == 'Pawn':
                totalWhite += 1
        
        for key in self.enemy.keys():
            if self.enemy[key] == 'King':
                totalBlack += 100
            if self.enemy[key] == 'Queen':
                totalBlack += 50
            if self.enemy[key] == 'Rook':
                totalBlack += 5
            if self.enemy[key] == 'Knight' or self.enemy[key] == 'Bishop':
                totalBlack += 3
            if self.enemy[key] == 'Pawn':
                totalBlack += 1

        return totalWhite - totalBlack, self.moveMade

    def isCheck(self, isMaxPlayer):
        if isMaxPlayer:
            for key in self.enemy.keys():
                posX = key[0]
                posY = key[1]

                if self.enemy[key] == 'King':
                    moves = self.movesKing(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Queen':
                    moves = self.movesQueen(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Bishop':
                    moves = self.movesBishop(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Knight':
                    moves = self.movesKnight(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Rook':
                    moves = self.movesRook(posX, posY, isMaxPlayer)
                elif self.enemy[key] == 'Pawn':
                    moves = self.movesPawn(posX, posY, isMaxPlayer)

                for move in moves:
                    mposX = move[0]
                    mposY = move[1]
                    mKey = (mposX, mposY)
                    if mKey in self.pieces.keys() and self.pieces[mKey] == 'King':
                        return True            
        else:
            for key in self.pieces.keys():
                posX = key[0]
                posY = key[1]

                if self.pieces[key] == 'King':
                    moves = self.movesKing(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Queen':
                    moves = self.movesQueen(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Bishop':
                    moves = self.movesBishop(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Knight':
                    moves = self.movesKnight(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Rook':
                    moves = self.movesRook(posX, posY, isMaxPlayer)
                elif self.pieces[key] == 'Pawn':
                    moves = self.movesPawn(posX, posY, isMaxPlayer)
                
                for move in moves:
                    mposX = move[0]
                    mposY = move[1]
                    mKey = (mposX, mposY)
                    if mKey in self.enemy.keys() and self.enemy[mKey] == 'King':
                        return True   
        return False

    def cutActions(self, actions, isMaxPlayer):
        new = []
        for action in actions:
            fromPos = action[0]
            toPos = action[1]
            newPieces = {**self.getPieces()}
            newEnemy = {**self.getEnemy()}
            newGame = Game(newPieces, newEnemy, [])

            if isMaxPlayer:
                piece = newGame.pieces[fromPos] # get name
                del newGame.pieces[fromPos] # del from old pos
                newGame.pieces[toPos] = piece # add to new pos
                if toPos in newGame.enemy.keys() and newGame.enemy[toPos] != 'King': # only can remove non kings
                    del newGame.enemy[toPos]
                if toPos in newGame.enemy.keys() and newGame.enemy[toPos] == 'King': # captured the king
                    del newGame.enemy[toPos]
                    hasWon = 1
                if not(newGame.isCheck(True)):
                    new.append(action)
            else:
                piece = newGame.enemy[fromPos]
                del newGame.enemy[fromPos]
                newGame.enemy[toPos] = piece
                if toPos in newGame.pieces.keys() and newGame.pieces[toPos] != 'King':
                    del newGame.pieces[toPos]
                if toPos in newGame.pieces.keys() and newGame.pieces[toPos] == 'King':
                    del newGame.enemy[toPos]
                    hasWon = -1
                if not(newGame.isCheck(False)):
                    new.append(action)
        return new

def abSearch(game):
    value, move = maxValue(game, 1, MININT, MAXINT)
    return move

def maxValue(game, depth, alpha, beta):
    if depth >= 3:
        return game.getValue()
    
    v = MININT
    actions = game.getSuccessor(True)
    move = []

    # if game.isCheck(True):
    #     actions = game.cutActions(actions, True)
    print(actions)
    for action in actions:
        newGame, hasWon = game.executeMove(action, True)
        if hasWon == -500:
            continue
        v2, a2 = minValue(newGame, depth + 1, alpha, beta)
        if v2 > v:
            v, move = v2, action
            alpha = max(alpha, v)
        if v >= beta:
            return v, move
    return v, move

def minValue(game, depth, alpha, beta):
    if depth >= 3:
        return game.getValue()

    v = MAXINT
    actions = game.getSuccessor(False)
    move = []
    # if game.isCheck(False):
    #     actions = game.cutActions(actions, False)
    for action in actions:
        newGame, hasWon = game.executeMove(action, False)
        if hasWon == -500:
            continue
        v2, a2 = maxValue(newGame, depth + 1, alpha, beta)
        if v2 < v:
            v, move = v2, action
            beta = min(beta, v)
        if v <= alpha:
            return v, move
    return v, move

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def toFinalFormat(game, result):
    aPosX1 = game.toAlphaPos(result[0][0])
    aPosX2 = game.toAlphaPos(result[1][0])
    final = [(aPosX1, result[0][1]), (aPosX2, result[1][1])]
    return final

def parseGameboard(game, gameboard):
    for key in gameboard.keys():
        isEnemy = False
        newKey = (game.toSingleNumPos(key[0]), key[1])
        value = gameboard[key]
        piece = value[0]
        if value[1] != 'White':
            isEnemy = True
        
        if isEnemy:
            game.enemy[newKey] = piece
        else:
            game.pieces[newKey] = piece

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    # config = sys.argv[1] #Takes in config.txt Optional
    game = Game({}, {}, [])
    parseGameboard(game, gameboard)

    move = abSearch(game)
    final = toFinalFormat(game, move)
    return final #Format to be returned (('a', 0), ('b', 3))

# s = studentAgent({('e', 0): ('King', 'White'), ('d', 0): ('Queen', 'White'), ('c', 0): ('Bishop', 'White'), ('b', 0): ('Knight', 'White'), ('a', 0): ('Rook', 'White'), ('a', 1): ('Pawn', 'White'), ('b', 1): ('Pawn', 'White'), ('c', 1): ('Pawn', 'White'), ('d', 1): ('Pawn', 'White'), ('e', 1): ('Pawn', 'White'), 
# ('e', 4): ('King', 'Black'), ('d', 4): ('Queen', 'Black'), ('c', 4): ('Bishop', 'Black'), ('b', 4): ('Knight', 'Black'), 
# ('a', 4): ('Rook', 'Black'), ('a', 3): ('Pawn', 'Black'), ('b', 3): ('Pawn', 'Black'), ('c', 3): ('Pawn', 'Black'), ('d', 3): ('Pawn', 'Black'), ('e', 3): ('Pawn', 'Black')})
s = studentAgent({('e', 0): ('King', 'White'), ('d', 0): ('Queen', 'White'), ('c', 0): ('Bishop', 'White'), ('b', 0): ('Knight', 'White'), ('a', 0): ('Rook', 'White'), ('a', 2): ('Pawn', 'White'), ('b', 1): ('Pawn', 'White'), ('d', 2): ('Pawn', 'White'), ('e', 1): ('Pawn', 'White'), 
('e', 4): ('King', 'Black'), ('d', 4): ('Queen', 'Black'), ('c', 4): ('Bishop', 'Black'), ('b', 4): ('Knight', 'Black'), 
('a', 4): ('Rook', 'Black'), ('a', 3): ('Pawn', 'Black'), ('b', 2): ('Pawn', 'Black'), ('d', 3): ('Pawn', 'Black'), ('e', 2): ('Pawn', 'Black')})
print(s)