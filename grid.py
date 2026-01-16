import numpy as np
import random
import pygame

class Grid:

    def render_font(self, screen, number, x, y):
        font = pygame.font.Font(None, 150)
        text_surface = font.render(str(int(number)), True, (255, 0, 0)) 
        text_rect = text_surface.get_rect(center=(x, y))

        screen.blit(text_surface, text_rect)


    def __init__(self, size = 4):
        self.__size = 4
        self.__grid = np.zeros((size, size))

        self.__directions = [-2, -1, 1, 2] # -2: left, 2: right, -1: down, 1: up

        self.__possible_generations = [2, 4]

    def draw(self, screen, color, bthickness, screen_dim):

        x, y = 0, 0
        side = screen_dim // self.__size
        for i in range(self.__size):
            for j in range(self.__size):
                pygame.draw.rect(screen, color, (x, y, side, side), bthickness)

                if self.__grid[i][j]:
                    self.render_font(screen, self.__grid[i][j], x + side // 2, y + side // 2)
            
                x += side
            x = 0
            y += side

    def get_board(self):
        return self.__grid

    def generate_block(self):
        idxs = []
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__grid[i][j] == 0:
                    idxs.append((i, j))

        if len(idxs) == 0:
            return "Game Over"


        x, y = random.choice(idxs)
        self.__grid[x][y] = random.choice(self.__possible_generations)

    def move(self, direction):

        prev_grid = self.__grid.copy()

        prev_merged = False
        for i in range(self.__size):
            new_arrangements = []
            for j in range(self.__size):

                if abs(direction) == 2:
                    x, y = i, j
                else:
                    x, y = j, i

                if self.__grid[x][y] == 0:
                    prev_merged = False
                    continue

                if not prev_merged and len(new_arrangements) > 0 and new_arrangements[-1] == self.__grid[x][y]:
                    new_arrangements[-1] *= 2
                    prev_merged = True
                else:
                    new_arrangements.append(self.__grid[x][y]);
                    prev_merged = False


            if direction < 0:
                for j in range(len(new_arrangements), self.__size):
                    new_arrangements.append(0);
            else:
                for j in range(len(new_arrangements), self.__size):
                    new_arrangements = [0] + new_arrangements

            
            if abs(direction) == 2:
                self.__grid[i] = new_arrangements
            else:
                self.__grid[:, i] = new_arrangements


        if np.array_equal(self.__grid, prev_grid):
            return False
        return True


