import sys
import copy
import random
import pygame
import numpy as np

from constants import *

# PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill( BACKGROUND_COLOR )

class Board():
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))

    def markSquare(self, row, col, player):
        self.squares[row][col] = player

    def isEmptySquare(self, row, col):
        return self.squares[row][col] == 0

class Game:

    def __init__(self):
        self.board = Board()
        # 1 Cross - 2 Circle
        self.player = 1
        self.showLines()

    def showLines(self):
        for i in range(1,10):
            # Vertical Lines
            pygame.draw.line(screen, LINE_COLOR, (WIDTH - (SQUARE_SIZE * i), 0), (WIDTH - (SQUARE_SIZE * i), HEIGHT), LINE_WIDTH)
            # Horizontal lines
            pygame.draw.line(screen, LINE_COLOR, (0, (HEIGHT - (SQUARE_SIZE * i))), (WIDTH, (HEIGHT - (SQUARE_SIZE * i))), LINE_WIDTH)

    def changePlayer(self):
        self.player = self.player % 2 + 1

    def drawFigure(self, row, col):
        if self.player == 1:
            # Draw cross
            # Descending line
            start_descending = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_descending = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_descending, end_descending, CROSS_WIDTH)
            # Ascending line
            start_ascending = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_ascending = (col * SQUARE_SIZE + SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_ascending, end_ascending, CROSS_WIDTH)
            
        elif self.player == 2:
            # Draw circle
            center = ( col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

def main():

    # Object
    game = Game()
    board = game.board

    #MainLoop
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.isEmptySquare(row, col):
                    board.markSquare(row, col, game.player)
                    game.drawFigure(row,col)
                    game.changePlayer()

        pygame.display.update()

main()