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
music_list = [
    "./assets/audio/NewsRoomNewsSpence.mp3",
    "./assets/audio/RussianDance-JoeyPecoraro.mp3",
    "./assets/audio/TakeMeDownToTheFashionShow-NoMBe.mp3",
    "./assets/audio/HimnoDeLaAlegria.mp3"
    ]
bubble_sound = pygame.mixer.Sound("./assets/audio/bubble.mp3")

class Board():
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))
        self.empty_squares = self.squares
        self.marked_squares = 0

    def finalState(self, row,col):
        """
        @return 0 if there was a draw.
        @return 1 if player 1 wins
        @return 2 if AI wins
        """

        for i in range(ROWS):
            for j in range(COLUMNS):
                if j <= COLUMNS-3:
                    if self.squares[i][j] == 1 and self.squares[i][j+1] == 1 and self.squares[i][j+2] == 1:
                        print("Toe horizontal")
                        self.squares[i][j] = 2
                        self.squares[i][j+1] = 2
                        self.squares[i][j+2] = 2
                        start_line = (j * SQUARE_SIZE + OFFSET_CENTER_2, i * SQUARE_SIZE + OFFSET_CENTER)
                        end_line = ((j+2) * SQUARE_SIZE + SQUARE_SIZE - OFFSET_CENTER_2, i * SQUARE_SIZE + OFFSET_CENTER)
                        pygame.draw.line(screen, LINE_CHECK_COLOR, start_line, end_line, LINE_CHECK_WIDTH)
                    if i <= ROWS-3:
                        if self.squares[i][j] == 1 and self.squares[i+1][j+1] == 1 and self.squares[i+2][j+2] ==1:
                            print("Toe Diagonal")
                            self.squares[i][j] = 3
                            self.squares[i+1][j+1] = 3
                            self.squares[i+2][j+2] = 3
                            start_line = (j * SQUARE_SIZE + OFFSET_CENTER, i * SQUARE_SIZE + OFFSET_CENTER)
                            end_line = ((j+2) * SQUARE_SIZE + SQUARE_SIZE - OFFSET_CENTER, (i+2) * SQUARE_SIZE + OFFSET_CENTER)
                            pygame.draw.line(screen, LINE_CHECK_COLOR, start_line, end_line, LINE_CHECK_WIDTH)
                if j >= 2:
                    if self.squares[i][j] == 1 and self.squares[i+1][j-1] == 1 and self.squares[i+2][j-2] == 1:
                        print("Toe diagonal invertida")
                        self.squares[i][j] = 4
                        self.squares[i+1][j-1] = 4
                        self.squares[i+2][j-2] = 4
                        start_line = (j * SQUARE_SIZE + OFFSET_CENTER, i * SQUARE_SIZE + OFFSET_CENTER)
                        end_line = ((j-2) * SQUARE_SIZE + SQUARE_SIZE - OFFSET_CENTER, (i+2) * SQUARE_SIZE + OFFSET_CENTER)
                        pygame.draw.line(screen, LINE_CHECK_COLOR, start_line, end_line, LINE_CHECK_WIDTH)
                if i <= ROWS-3:
                    if self.squares[i][j] == 1 and self.squares[i+1][j] == 1 and self.squares[i+2][j] == 1:
                        print("Toe Vertical")
                        self.squares[i][j] = 5
                        self.squares[i+1][j] = 5
                        self.squares[i+2][j] = 5
                        start_line = (j * SQUARE_SIZE + OFFSET_CENTER, i * SQUARE_SIZE + OFFSET_CENTER)
                        end_line = (j * SQUARE_SIZE + SQUARE_SIZE - OFFSET_CENTER, (i+2) * SQUARE_SIZE + OFFSET_CENTER)
                        pygame.draw.line(screen, LINE_CHECK_COLOR, start_line, end_line, LINE_CHECK_WIDTH)
        # Draw
        return 0

    def markSquare(self, row, col, player):
        self.squares[row][col] = player
        self.marked_squares += 1

    def isEmptySquare(self, row, col):
        return self.squares[row][col] == 0

    def getEmptySquares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.isEmptySquare(row, col):
                    empty_squares.append( (row,col) )
        return empty_squares

    def isFull(self):
        return self.marked_squares == 100

    def isEmpty(self):
        return self.marked_squares == 0

class AI():
    def __init__(self, level=0, player=2):
        self.level = level
        self.player = player

    def random(self, board):
        empty_squares = board.getEmptySquares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index] # (row,col)

    def minimax(self, board, maximizing):
        # Terminal case
        case = board.finalState()

        # Player 1 wins
        if case == 1:
            return 1, None # Eval, move

        # Player 2 wins
        if case == 2:
            return -1, None
        
        # Draw
        elif board.isFull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.getEmptySquares()

            for(row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.markSquare(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_squares = board.getEmptySquares()

            for(row,col) in empty_squares:
                temp_board = copy.deepcopy(board)
                temp_board.markSquare(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = 'random'
            move = self.random(main_board)
        else:
            # Minimax algorithm choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1 # 1 Cross - 2 Circle
        self.gameMode = "ai" # pvp or ai
        self.running = True
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

            pygame.mixer.Sound.play(bubble_sound)

        elif self.player == 2:
            # Draw circle
            center = ( col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

def main():

    # Object
    game = Game()
    board = game.board
    ai = game.ai
    music = random.choice(music_list)
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

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

        if game.gameMode == 'ai' and game.player == ai.player:
            pygame.display.update()

            # AI methods
            row, col = ai.eval(board)

            board.markSquare(row, col, ai.player)
            board.finalState(row,col)
            game.drawFigure(row,col)
            game.changePlayer()

        pygame.display.update()

main()