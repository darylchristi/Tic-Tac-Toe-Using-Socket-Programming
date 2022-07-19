import pygame
import os
from tkinter import *
from tkinter import messagebox

window = Tk()
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
window.withdraw()

letterX = pygame.image.load(os.path.join('images', 'X.png'))
letterO = pygame.image.load(os.path.join('images', 'O.png'))


class Grid:
    def __init__(self):
        self.grid_lines = [((0, 200), (600, 200)),  # first horizontal line
                           ((0, 400), (600, 400)),  # second horizontal line
                           ((200, 0), (200, 600)),  # first vertical line
                           ((400, 0), (400, 600))]  # second vertical line

        self.grid = [[0 for x in range(3)] for y in range(3)]
        # search directions  N         NW        W       SW       S       SE      E       NE
        self.search_direction = [(0, -1), (-1, -1), (-1, 0),
                                 (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (200, 200, 200), line[0], line[1], 2)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == "X":
                    surface.blit(letterX, (x*200, y*200))
                elif self.get_cell_value(x, y) == "O":
                    surface.blit(letterO, (x*200, y*200))

    def get_cell_value(self, x, y):
        return self.grid[y][x]

    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
            self.switch_player = True
            if player == "X":
                self.set_cell_value(x, y, "X")
            elif player == "O":
                self.set_cell_value(x, y, "O")
            self.check_grid(x, y, player)
        else:
            self.switch_player = False

    def is_within_bounds(self, x, y):
        return x >= 0 and x < 3 and y >= 0 and y < 3

    def check_grid(self, x, y, player):
        count = 1
        for index, (dirx, diry) in enumerate(self.search_direction):
            if self.is_within_bounds(x+dirx, y+diry) and self.get_cell_value(x+dirx, y+diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.is_within_bounds(xx+dirx, yy+diry) and self.get_cell_value(xx+dirx, yy+diry) == player:
                    count += 1
                    if count == 3:
                        break

                if count < 3:
                    new_direction = 0
                    # mapping

                    if index == 0:
                        new_direction = self.search_direction[4]  # N to S
                    elif index == 1:
                        new_direction = self.search_direction[5]  # NW to SE
                    elif index == 2:
                        new_direction = self.search_direction[6]  # W to E
                    elif index == 3:
                        new_direction = self.search_direction[7]  # SW to NE
                    elif index == 4:
                        new_direction = self.search_direction[0]  # S to N
                    elif index == 5:
                        new_direction = self.search_direction[1]  # SE to NW
                    elif index == 6:
                        new_direction = self.search_direction[2]  # E to W
                    elif index == 7:
                        new_direction = self.search_direction[3]  # NE to SW

                    if self.is_within_bounds(x + new_direction[0], y + new_direction[1]) \
                            and self.get_cell_value(x + new_direction[0], y + new_direction[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1
        if count == 3:  # Win condition 3 in a row
            messagebox.showinfo("Game Over", f"{player} Wins!")

            window.quit()
            #print(player, 'wins!')
            self.game_over = True
        else:
            self.game_over = self.is_grid_full()

    def is_grid_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False

        messagebox.showinfo('Game Over',
                            'Match DRAW')  # Draw condition

        window.quit()
        self.game_over = True
        return True

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def print_grid(self):
        for row in self.grid:
            print(row)
