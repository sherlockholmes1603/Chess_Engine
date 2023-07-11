'''It is our main driver file. It will be used for handelling user input and displaying the current GameState Objective'''


import pygame as p
import chessEngine

WIDTH = HEIGTH = 512
DIMENSION = 8
SQ_SIZE = HEIGTH//DIMENSION
MAX_FPS = 15
IMAGES = {}

#initialize a global dictionary of images
def load_images():
    pieces = ["bP", "bR", "bN", "bB", "bQ", "bK", "wP", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale( p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


'''Responsible for all the graphics within the current game state'''
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

'''Draw the sqaures on the board'''
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE) )


'''Draw The pieces of the chess'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''The main driver for our code. This will handle user input and updating the graphics'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    load_images() # This has to be called one time only
    running = True
    sqSelected = ()
    playerClick = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClick = []
                else:
                    sqSelected = (row, col)
                    playerClick.append(sqSelected)
                if len(playerClick) == 2:
                    move = chessEngine.Move(playerClick[0], playerClick[1], gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        print(move.getChessNotation())
                        sqSelected = ()
                        playerClick = []
                    else:
                        print("Not a Valid Move")
                        r = sqSelected[0]
                        c = sqSelected[1]
                        if(gs.board[r][c] != "--"):
                            playerClick = [sqSelected]
                        else:
                            playerClick = []
            
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            
        
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


if __name__ == "__main__":
    main()


