from const import *
from square import Square
from pieces import *
from move import Move

class Board():

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0 ] for col in range(COLS)]
        self.last_move = None
        self.create()
        self.add_pieces("white")
        self.add_pieces("black")

        

    def create(self):
        

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def calc_moves(self, piece,  row, col):
        
        
        
        def knight_moves():
            # print(piece.name)
            # print(row, col, piece.color)
            possible_moves =  [
                (row-2, col+1),
                (row+2, col+1),
                (row-2, col-1),
                (row+2, col-1),
                (row-1, col+2),
                (row+1, col+2),
                (row-1, col-2),
                (row+1, col-2)
            ]

            for possible in possible_moves:
                p_row, p_col = possible

                if Square.in_range(p_row, p_col):
                    if self.squares[p_row][p_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(p_row, p_col)
                        move = Move(initial, final)
                        
                        piece.add_move(move)
                
        def pawn_moves():
            steps = 1 if piece.moved else 2

            start = row + piece.dir
            end = row + (piece.dir * (1+steps))

            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isEmpty():
                        initial = Square(row, col)
                        final = Square(move_row, col)

                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
            p_row = row+piece.dir
            p_col = [col-1, col+1]
            for poss_col in p_col:
                if(Square.in_range(p_row, poss_col)):
                    if self.squares[p_row][poss_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(p_row, poss_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                p_row = row + row_incr
                p_col = col + col_incr

                while True:
                    if Square.in_range(p_row, p_col):
                        initial = Square(row, col)
                        final = Square(p_row, p_col)

                        move = Move(initial, final)

                        if self.squares[p_row][p_col].isEmpty():
                            piece.add_move(move)

                        if self.squares[p_row][p_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break

                        if self.squares[p_row][p_col].has_team_piece(piece.color):
                            break

                        p_row = p_row + row_incr
                        p_col = p_col + col_incr
                    else:
                        break

        def king_moves():
            possible_moves =  [
                (row-1, col+1),
                (row+1, col+1),
                (row-1, col-1),
                (row+1, col-1),
                (row, col+1),
                (row+1, col),
                (row-1, col),
                (row, col-1)
            ]

            for possible in possible_moves:
                p_row, p_col = possible

                if Square.in_range(p_row, p_col):
                    if self.squares[p_row][p_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(p_row, p_col)
                        move = Move(initial, final)
                        
                        piece.add_move(move)

            if not piece.moved:

                left_rook = self.squares[row][0].piece

                if isinstance(left_rook, Rook):
                    if not left_rook:
                        for c in range(1, 4):
                            if self.squares[row][col].has_piece():
                                break

        
        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straight_line_moves([(1, 1), 
                                 (1, -1), 
                                 (-1, 1), 
                                 (-1, -1)])
        elif isinstance(piece, Rook):
            straight_line_moves([(1, 0), 
                                 (0, -1), 
                                 (-1, 0), 
                                 (0, 1)])
        elif isinstance(piece, Queen):
            straight_line_moves([(1, 1), 
                                 (1, -1), 
                                 (-1, 1), 
                                 (-1, -1)])
            straight_line_moves([(1, 0), 
                                 (0, -1), 
                                 (-1, 0), 
                                 (0, 1)])
        elif isinstance(piece, King):
            king_moves()

    
    def move(self,piece, move):
        initial = move.initial
        final = move.final

        self.squares[initial.r][initial.c].piece = None
        self.squares[final.r][final.c].piece = piece

        if isinstance(piece, Pawn):
            self.checkPromotion(piece, final)

        piece.moved = True

        piece.clear_moves()

        self.last_move = move

    def checkPromotion(self, piece, final):
        if final.r == 0 or final.r == 7:
            self.squares[final.r][final.c].piece = Queen(piece.color)
    
    def valid_move(self,piece, move):
        return move in piece.moves 

    def castling(self, initial, final):
        pass

    def add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color=="white" else (1, 0)


        #Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))


        #Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        #Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #Rook
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        








