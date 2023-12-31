import pygame
import sys
from  game import Game
from const import *
from dragger import Dragger
from square import Square
from move import Move


class Main():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        self.game = Game()
        self.dragger = Dragger()

    def mainloop(self):
        clock = pygame.time.Clock()

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:

            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if game.board.squares[clicked_row][clicked_col].has_piece():
                        piece = game.board.squares[clicked_row][clicked_col].piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                        game.show_bg(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)


                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY//SQSIZE
                        released_col = dragger.mouseX//SQSIZE

                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)

                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()

                            board.move(dragger.piece, move)

                            game.sound_effect(captured)

                            game.show_bg(screen)
                            game.show_pieces(screen)

                            game.next_turn()
                    
                    dragger.undrag_piece()
                
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                

            

            pygame.display.update()


main = Main()
main.mainloop()