# Author:Stew Towle
# Date: November 2022
# Description: This script contains the GUI for playing Janggi using my original Janggi program
#       It utilizes pygame to make the gui.

import pygame as pg
import JanggiGame as jg

FRAME_RATE = 15


class JanggiGui:
    """
    Contains the GUI for playing Janggi
    """



    def __init__(self, width=None, height=None):
        self.game = jg.JanggiGame()
        self.WIDTH = 450 if width is None else width
        self.HEIGHT = 500 if height is None else height
        self.PADDING = 45
        self.SIDE_PADDING = 8
        self.CELL_SIZE = self.HEIGHT // 10  #10 here because there are 10 rows in Janggi

    def run(self):
        """Runs a fresh game"""
        pg.init()
        screen = pg.display.set_mode((self.WIDTH + (2 * self.SIDE_PADDING), self.PADDING + self.HEIGHT + (2 * self.SIDE_PADDING)))
        clock = pg.time.Clock()
        screen.fill(pg.Color("gray"))
        self.draw_board(screen)
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.draw_game(screen)
            clock.tick(FRAME_RATE)
            pg.display.flip()

    def draw_game(self, screen):
        print("draw game is running")
        #self.draw_board(screen)

    def draw_pieces(self):
        print("draw pieces is running")

    def draw_board(self, screen):
        print("draw board is running")
        game_board = self.game.get_board()
        pg.draw.rect(screen, pg.Color("black"), pg.Rect(0, self.PADDING, len(game_board[0])*self.CELL_SIZE + 2*self.SIDE_PADDING,
                                                        len(game_board)*self.CELL_SIZE + 2 * self.SIDE_PADDING), self.SIDE_PADDING)
        for i in range(len(game_board)):
            for j in range(len(game_board[0])):
                #make every other square white
                if (i + j) % 2 == 0:
                    print("rect", i, j)
                    pg.draw.rect(screen, pg.Color("white"), \
                                 pg.Rect(self.SIDE_PADDING + j*self.CELL_SIZE,
                                         self.PADDING + self.SIDE_PADDING + (i*self.CELL_SIZE),
                                         self.CELL_SIZE, self.CELL_SIZE))





def main():
    """starts a fresh game"""
    game = JanggiGui()
    game.run()

if __name__ == "__main__":
    main()