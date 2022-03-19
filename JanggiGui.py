# Author:Stew Towle
# Date: November 2022
# Description: This script contains the GUI for playing Janggi using my original Janggi program
#       It utilizes pygame to make the gui.

import pygame as pg
import JanggiGame as jg
import JanggiAi as ai
import random

FRAME_RATE = 15
BOARD_DARK = pg.Color("dark gray")
BOARD_LIGHT = pg.Color("white")
BG_COL = pg.Color("gray")
TEXT_COL = pg.Color("indigo")


class JanggiGui:
    """
    Contains the GUI for playing Janggi
    """

    def __init__(self, size=None):
        """"""
        self.game = jg.JanggiGame()
        self.WIDTH = 760 if size is None else size
        self.HEIGHT = (self.WIDTH / 9) * 10
        self.col_conversion = self.game.get_col_conv()

        self.SIDE_PADDING = 8
        self.CELL_SIZE = self.WIDTH / 9  #10 here because there are 10 rows in Janggi
        self.PADDING = self.CELL_SIZE
        self.piece_selected = None
        self.last_move_valid = True

    def run(self):
        """Runs a fresh game"""
        pg.init()
        random.seed()
        screen = pg.display.set_mode((self.WIDTH + (2 * self.SIDE_PADDING), self.PADDING + self.HEIGHT + (2 * self.SIDE_PADDING)))
        clock = pg.time.Clock()
        screen.fill(pg.Color("gray"))
        self.draw_game(screen)
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not self.piece_selected:
                        attempt = self.get_click_location(pg.mouse.get_pos())
                        if self.game.get_board()[attempt[0]][attempt[1]]:
                            self.piece_selected = attempt
                    else:
                        self.attempt_move(self.piece_selected, self.get_click_location(pg.mouse.get_pos()))
                        self.piece_selected = None

            if self.game.get_whose_turn() == 'red':
                potential_moves = ai.ai_move_simple(self.game, 'red')
                if not potential_moves:
                    print("NO VALID MOVES FOR AI - red")
                else:
                    current_move = potential_moves[0]
                    top_val = current_move[0]
                    choices = [current_move]
                    for move in potential_moves:
                        if move[0] > top_val:
                            break
                        choices.append(move)
                    current_move = choices[random.randrange(len(choices))]
                    clock.tick(5)
                    self.piece_selected = (int(current_move[1][1:])-1, self.col_conversion[current_move[1][0]])
                    self.draw_game(screen)
                    clock.tick(FRAME_RATE)
                    pg.display.flip()
                    clock.tick(1)

                    self.game.make_move(current_move[1], current_move[2])
                    self.piece_selected = None


            self.draw_game(screen)
            clock.tick(FRAME_RATE)
            pg.display.flip()


    def get_click_location(self, mouse_pos):
        """Returns location as row, col (which is reversed to how pygame handles things, but matches janggiGame)"""
        col = (mouse_pos[0] - self.SIDE_PADDING) // self.CELL_SIZE
        row = (mouse_pos[1] - self.SIDE_PADDING - self.PADDING) // self.CELL_SIZE
        return (int(row), int(col))

    def attempt_move(self, source, dest):
        src_str = self.game.convert_loc_to_str(source[0], source[1])
        dest_str = self.game.convert_loc_to_str(dest[0], dest[1])
        if src_str != dest_str:
            self.last_move_valid = self.game.make_move(src_str, dest_str)

#############DRAWING BOARD LOGIC###################
    def draw_game(self, screen):
        """Draws the entire game"""
        self.draw_board(screen)
        self.draw_pieces(screen)
        self.draw_text_info(screen)

    def draw_text_info(self, screen):
        a_font = pg.font.Font(None, int(self.CELL_SIZE // 2))
        if self.game.get_game_state() == 'UNFINISHED':
            text = a_font.render(f"It is {self.game.get_whose_turn()} player's turn.", False, TEXT_COL)
        else:
            text = a_font.render(f"The game is over: {self.game.get_game_state()}.", False, TEXT_COL)
        screen.blit(text, (0,0))

    def draw_pieces(self, screen):
        """Draws the game pieces onto the board"""
        game_board = self.game.get_board()
        for row_index, row in enumerate(game_board):
            for col_index, piece in enumerate(row):
                if piece:
                    self.draw_a_piece(screen, row_index, col_index, piece)

    def draw_a_piece(self, screen, row, col, piece):
        """Given a row, column and JanggiPiece object draws it in the appropriate square"""
        color = piece.get_color()
        half_cell = self.CELL_SIZE / 2
        center = (self.SIDE_PADDING + (col * self.CELL_SIZE) + half_cell,
                  self.PADDING + self.SIDE_PADDING + (row * self.CELL_SIZE) + half_cell)
        if piece.get_name() == "GENERAL":
            pg.draw.circle(screen, pg.Color("gold"), center, half_cell)
        circle = pg.draw.circle(screen, color, center, half_cell - 3)
        the_font = pg.font.Font(None, int(half_cell))
        text = the_font.render(piece.get_name()[:3], False, pg.Color("white"))
        text_size = text.get_size()
        text_placement = (center[0] - (text_size[0] / 2), center[1] - (text_size[1] / 2))
        screen.blit(text, text_placement)

    def draw_board(self, screen):
        """Draws the squares of the board with outline and highlights selected square"""
        pg.draw.rect(screen, BG_COL, pg.Rect(0, 0, self.WIDTH, self.HEIGHT))
        game_board = self.game.get_board()
        pg.draw.rect(screen, pg.Color("black"), pg.Rect(0, self.PADDING, len(game_board[0])*self.CELL_SIZE + (2 * self.SIDE_PADDING),
                                                        len(game_board)*self.CELL_SIZE + (2 * self.SIDE_PADDING)), self.SIDE_PADDING)
        for i in range(len(game_board)):
            for j in range(len(game_board[0])):
                #highlight selected piece
                if self.piece_selected and self.should_highlight(i, j):
                    pg.draw.rect(screen, pg.Color("light green"),
                                 pg.Rect(self.SIDE_PADDING + (j * self.CELL_SIZE),
                                         self.PADDING + self.SIDE_PADDING + (i * self.CELL_SIZE),
                                         self.CELL_SIZE, self.CELL_SIZE))
                # make every other square white
                elif (i + j) % 2 == 0:
                    pg.draw.rect(screen, BOARD_LIGHT,
                                 pg.Rect(self.SIDE_PADDING + (j*self.CELL_SIZE),
                                         self.PADDING + self.SIDE_PADDING + (i*self.CELL_SIZE),
                                         self.CELL_SIZE, self.CELL_SIZE))
                else:
                    pg.draw.rect(screen, BOARD_DARK,
                                 pg.Rect(self.SIDE_PADDING + (j * self.CELL_SIZE),
                                         self.PADDING + self.SIDE_PADDING + (i * self.CELL_SIZE),
                                         self.CELL_SIZE, self.CELL_SIZE))


    def should_highlight(self, i, j):
        if i == self.piece_selected[0] and j == self.piece_selected[1]:
            return True
        list_potentials = self.game.list_moves(self.piece_selected)
        if self.game.convert_loc_to_str(i,j) in list_potentials:
            return True
        return False



def main():
    """starts a fresh game"""
    game = JanggiGui()
    game.run()

if __name__ == "__main__":
    main()