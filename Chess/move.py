

class Move():

    def __init__(self, initial, final):
        self.initial = initial # Initial position of the piece (row and column) in tuple format: (r, c).
        self.final = final  # Final position of the piece after move is made

    def __str__(self) -> str:
        s = ''
        s += f'({self.initial.c}, {self.initial.r})'
        s += f' -> ({self.final.c}, {self.final.r})'
        return s
    
    def __eq__(self,object) -> bool:
        print(object)
        return self.initial == object.initial and self.final == object.final