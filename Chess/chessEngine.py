''' This is responsible for storing all the information about the current state of chess game '''

class GameState():
    def __init__(self):
        ''' This is representation of the 8 by 8 chess board
        If        the string is "--" then the cell is empty
        Otherwise it represents what piece occupies that square (e.g., wP) 
        The first row contains black pieces(bishop, nknight, rook, queen, king) and second black pawns
        Last column contains white pieces in same order as above and second last coloumn contains balck pawns

        '''
        
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.whiteToMove = True
        self.moveLog = []
        self.enPassantTargetSquare = None
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.incheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enPassantPossible = ()

    
    def makeMove(self, move):
        '''Take a move as parameter and execute it'''
        self.board[move.sRow][move.sCol] = "--"
        self.board[move.eRow][move.eCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove 
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.eRow, move.eCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.eRow, move.eCol)

        if move.isPawnPromotion:
            self.board[move.eRow][move.eCol] = move.pieceMoved[0] + 'Q'
        print(move.isEnPassantMove)
        if move.isEnPassantMove:
            self.board[move.sRow][move.eCol] = '--'
            print(move.sRow, move.sCol, move.eRow, move.eCol)

        if move.pieceMoved[1] == 'P' and abs(move.sRow - move.eRow) == 2:
            self.enPassantPossible = ((move.sRow + move.eRow)//2, move.sCol)
        else:
            self.enPassantPossible = ()
    
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.sRow][move.sCol] = move.pieceMoved
            self.board[move.eRow][move.eCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove 
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.sRow, move.sCol)
            elif  move.pieceMoved == 'bK':
                self.blackKingLocation = (move.sRow, move.sCol)
            
            if move.isEnPassantMove:
                self.board[move.eRow][move.eCol] = '--'
                self.board[move.sRow][move.sCol] = move.pieceCaptured
                self.enPassantPossible = (move.eRow, move.sCol)
            
            if move.pieceMoved[1] == 'P' and abs(move.sRow - move.eRow) == 2:
                self.enPassantPossible = ()

    def getValidMoves(self):
        self.incheck, self.pins, self.checks = self.checkforPinsChecks()
        if self.whiteToMove:
            kRow, kCol = self.whiteKingLocation
        else:
            kRow,kCol= self.blackKingLocation
        
        if self.incheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validS = (kRow + check[2]*i, kCol + check[3]*i)
                        validSquares.append(validS)
                        if validS[0] == checkRow and validS[1] == checkCol:
                            break
                
                for i in range(len(moves)-1, -1, -1):
                    if(moves[i].pieceMoved != 'K'):
                        if not (moves[i].eRow, moves[i].eCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kRow, kCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.incheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False


        return moves
    
    def checkforPinsChecks(self):
        pins = []
        checks = []
        incheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = "w"
            sRow, sCol = self.whiteKingLocation
        else: 
            allyColor = 'b'
            enemyColor="w"
            sRow, sCol = self.blackKingLocation

        directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)):
            d = directions[j]

            possiblePins = ()

            for i in range(1, 8):
                eRow = sRow +d[0]*i
                eCol=sCol+d[1]*i

                if 0<= eRow<8 and 0<=eCol<8:
                    endPiece = self.board[eRow][eCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePins == ():
                            possiblePins = (eRow, eCol, d[0], d[1])
                        else:
                            break
                    
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]

                        if( 0<= j <=3 and type == 'R') or (4<=j<=7 and type == 'B') or \
                        (i==1 and type == "P" and ((enemyColor=='w' and 6<=j<=7) or (enemyColor=='b' and 4<=j<=5))) or \
                        (type == 'Q') or (i==1 and type == 'K'):
                            if possiblePins == ():
                                incheck = True
                                checks.append((eRow, eCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePins)
                                break
                        else:
                            break

        #For knight check
        knightMoves = ((2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))

        for m in knightMoves:
            eRow = sRow + m[0]
            eCol = sCol + m[1]
            if 0<= eRow <= 7 and 0<= eCol <=7:
                endPiece = self.board[eRow][eCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":
                    incheck = True
                    checks.append((eRow, eCol, m[0], m[1]))

        return incheck, pins, checks
                    
                    



    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                turn = self.board[r][c][0]
                if (turn=="w" and self.whiteToMove) or (turn=="b" and not self.whiteToMove):
                    piece = self.board[r][c][1]

                    if piece == "P":
                        self.getPawnMoves(r, c, moves)

                    elif piece == "R":
                        self.getRookMoves(r, c, moves)

                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)

                    elif piece == "Q":
                        self.getQueenMoves(r, c, moves)

                    elif piece == "K":
                        self.getKingMoves(r, c, moves)

                    elif piece == "N":
                        self.getNknightMoves(r, c, moves)

        
        return moves
    

    




    def getPawnMoves(self, r, c, moves):
        
        peicepinned = False
        pinDirection = ()
        for i in range(len(self.pins) -1,-1,-1):
            if self.pins[i][0] ==r and self.pins[i][1] == c:
                peicepinned= True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not peicepinned or pinDirection == (-1, 0):
                    moves.append(Move((r,c), (r-1, c), self.board))
                    if r==6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c), self.board))

            if not peicepinned or pinDirection == (-1, -1):
                if c>0 and self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c),(r-1,c-1), self.board))
                elif (r-1, c-1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r-1,c-1), self.board, enPassantPossible=True))
            
            if not peicepinned or pinDirection == (-1, 1):
                if c<7 and self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c),(r-1,c+1), self.board))
                elif (r-1, c+1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r-1,c+1), self.board, enPassantPossible=True))

        else:
            if self.board[r+1][c] == "--":
                if not peicepinned or pinDirection == (1, 0):
                    moves.append(Move((r,c), (r+1, c), self.board))
                    if r==1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2,c), self.board))

            if not peicepinned or pinDirection == (1, -1):
                if c>0 and self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c),(r+1,c-1), self.board))
                elif (r+1, c-1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r+1,c-1), self.board, enPassantPossible=True))
            
            if not peicepinned or pinDirection == (1, 1):
                if c<7 and self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c),(r+1,c+1), self.board))
                elif (r+1, c+1) == self.enPassantPossible:
                    moves.append(Move((r,c),(r+1,c+1), self.board, enPassantPossible=True))

    def getRookMoves(self, r, c, moves):
        piecepinned = False
        pindirection = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecepinned = True
                pindirection = tuple(self.pins[i])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        #
        
        direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
        enemyCol = "b" if self.whiteToMove else "w"
        for d in direction:
            for i in range(1, 8):
                row = r + d[0]*i
                col = c + d[1]*i
                if 0<= row<8 and 0<=col<8:
                    if not piecepinned or pindirection == d or pindirection==(-d[0], -d[1]):
                        endPiece = self.board[row][col]
                        if endPiece == "--":
                            moves.append(Move((r,c), (row, col), self.board))
                        elif endPiece[0] == enemyCol:
                            moves.append(Move((r,c), (row, col), self.board))
                            break 
                        else:
                            break
                else:
                    break

    

    def getBishopMoves(self, r, c, moves):
        piecepinned = False
        pindirection = ()

        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecepinned = True
                pindirection = tuple(self.pins[i])
                self.pins.remove(self.pins[i])
                break


        direction = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        enemyCol = "b" if self.whiteToMove else "w"
        for d in direction:
            for i in range(1, 8):
                row = r + d[0]*i
                col = c + d[1]*i
                if 0<= row<8 and 0<=col<8:
                    if not piecepinned or pindirection == d or pindirection==(-d[0], -d[1]):
                        endPiece = self.board[row][col]
                        if endPiece == "--":
                            moves.append(Move((r,c), (row, col), self.board))
                        elif endPiece[0] == enemyCol:
                            moves.append(Move((r,c), (row, col), self.board))
                            break 
                        else:
                            break
                else:
                    break

    def getNknightMoves(self, r, c, moves):

        peicepinned = False
        
        for i in range(len(self.pins) -1,-1,-1):
            if self.pins[i][0] ==r and self.pins[i][1] == c:
                peicepinned= True
                self.pins.remove(self.pins[i])
                break

        direction = ((2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2))
        allyCol = "w" if self.whiteToMove else "b"
        for d in direction:
            row = r + d[0]
            col = c + d[1]
            if 0 <= row < 8 and 0 <= col < 8:
                if not peicepinned:
                    endPiece = self.board[row][col][0]
                    if endPiece!=  allyCol:
                        moves.append(Move((r,c), (row, col), self.board))
    
    def getKingMoves(self, r, c, moves):
        direction = ((1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1))
        allyCol = "w" if self.whiteToMove else "b"
        for d in direction:
            erow = r + d[0]
            ecol = c + d[1]
            if 0 <= erow < 8 and 0 <= ecol < 8:
                endPiece = self.board[erow][ecol][0]
                if endPiece!=  allyCol:
                    
                    if allyCol == 'w':
                        self.whiteKingLocation = (erow, ecol)
                    else:
                        self.blackKingLocation = (erow, ecol)
                    
                    incheck, pins, check = self.checkforPinsChecks()

                    if not incheck:
                        moves.append(Move((r,c), (erow, ecol), self.board))
                    
                    if allyCol == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)


    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)
        

    



class Move():

    
    ranksToRows = {"1" :7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k,v in ranksToRows.items()}

    filesToCols = {"h" :7, "g":6, "f":5, "e":4, "d":3, "c":2, "b":1, "a":0}
    colsToFiles = {v: k for k,v in filesToCols.items()}
    
    def __init__(self, startSq, endSq, board, enPassantPossible = False):
        self.sRow = startSq[0]
        self.sCol = startSq[1]
        self.eRow = endSq[0]
        self.eCol = endSq[1]
        self.pieceMoved = board[self.sRow][self.sCol]
        self.pieceCaptured = board[self.eRow][self.eCol]
        self.moveID = 1000*self.sRow + 100*self.sCol + 10*self.eRow + self.eCol
        self.isPawnPromotion = False

        self.promotionChoice = 'Q'

        if (self.pieceMoved == 'wP' and self.eRow==0) or (self.pieceMoved == 'bP' and self.eRow == 7):
            self.isPawnPromotion = True

        self.isEnPassantMove = enPassantPossible
        if self.isEnPassantMove:
            print(startSq, endSq)
        if self.isEnPassantMove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
        

    
    def __eq__(self,object):
        if(isinstance(object, Move)):
            return self.moveID == object.moveID
        return False
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
    
    def getChessNotation(self):
        return self.pieceMoved + self.getRankFile(self.eRow, self.eCol)








