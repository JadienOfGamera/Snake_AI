from random import randint
import pygame, sys
import Snake

#Grid => 0 : Empty | 1 : Apple | 2 : Snake

class GridCell:
    def __init__(self, cell, value):
        self.cell = cell
        self.value = value


class Grid:
    def __init__(self, size_x, size_y, screen):
        self.size_x = size_x
        self.size_y = size_y
        self.screen = screen

        self.grid = [[0 for x in range(size_y)] for y in range(size_x)]
        self.apple_pos_x = randint(0, size_x - 1)
        self.apple_pos_y = randint(0, size_y - 1)

        self.grid[self.apple_pos_x][self.apple_pos_y] = 1

        self.grid_cell = [[]]
        
        for case_x in range(self.size_y):
            for case_y in range(self.size_x):
                print(self.grid[case_x][case_y], end="")
            print("")


    def draw_grid(self):
        for x in range(self.size_x):
            row = []
            for y in range(self.size_y):
                rect = pygame.Rect(x * margin, y * margin, margin, margin)
                if self.grid[x][y] == 0:
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
                    row.append(GridCell(rect, 0))
                elif self.grid[x][y] == 1:
                    pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    row.append(GridCell(rect, 1))
            self.grid_cell.append(row)
        pygame.display.update()


if __name__ == '__main__':
    
    size_x = 20
    size_y = 20
    margin = 40
    WIDTH = size_x * margin
    HEIGHT = size_y * margin

    snake = Snake(size_x, size_y)
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    grid = Grid(size_x, size_y, screen)

    running = True
    grid.draw_grid()
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False