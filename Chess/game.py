#Responsible for the rendering of the game

from const import *
import pygame
from board import Board
from dragger import Dragger
from pieces import *
from config import Config

class Game():

    def __init__(self):
        self.board = Board()
        self.hovered_sq = None
        self.dragger = Dragger()
        self.next_player = 'white'
        self.config = Config()



    def show_bg(self, screen):
        theme = self.config.theme


        for row in range(ROWS):
            for col in range(COLS):

                color = theme.bg.light if (row + col) %2 ==0 else theme.bg.dark
                
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(screen, color, rect)

    
    def show_pieces(self, screen):
        #Draw pieces on top of background and other pieces
        for row in range(ROWS):
            for col in range(COLS):

                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece: 
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_centre = col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center= img_centre)
                        screen.blit(img, piece.texture_rect)

    def show_moves(self, screen):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            # print(piece.moves)

            for move in piece.moves:
                color = theme.move.light if (move.final.r + move.final.c) %2 ==0 else theme.move.dark
                rect = (move.final.c * SQSIZE, move.final.r * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(screen, color, rect)

    def show_last_move(self, screen):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final   = self.board.last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.r + pos.c) %2 == 0 else theme.trace.dark
                rect = (pos.c*SQSIZE, pos.r*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(screen, color, rect)
                
    
    def show_hover(self, screen):
        if self.hovered_sq:
            color = (180, 180, 180)
            rect = (self.hovered_sq.c*SQSIZE, self.hovered_sq.r*SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(screen, color, rect)
    
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sq = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
