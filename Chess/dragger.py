import pygame
from const import *

class Dragger():

    def __init__(self):
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.dragging = False
        self.initial_col = 0

    def update_blit(self, screen):
        self.piece.set_texture(size = 128)
        texture = self.piece.texture

        img = pygame.image.load(texture)
        image_centre = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center = image_centre)
        screen.blit(img, self.piece.texture_rect)
    
    def update_mouse(self, pos):
        self.mouseX = pos[0]
        self.mouseY = pos[1]

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False