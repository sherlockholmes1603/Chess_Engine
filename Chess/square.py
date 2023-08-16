



class Square():

    def __init__(self, r, c, piece = None):
        self.r = r
        self.c = c
        self.piece = piece

    def __eq__(self,object) -> bool:
        return self.r == object.r and self.c == object.c

    def has_piece(self):
        return self.piece != None
    
    def isEmpty(self):
        return not self.has_piece()
    
    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def isempty_or_rival(self, color):
        return self.isEmpty() or self.has_rival_piece(color)
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg<0 or arg>7:
                return False
            
        return True
    
