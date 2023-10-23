from random import randint
import pygame, sys


#Grid => 0 : Empty | 1 : Apple | 2 : Snake

class Grid:
    def __init__(self, size_x, size_y, margin, screen):
        self.size_x = size_x
        self.size_y = size_y
        self.margin = margin
        self.screen = screen

        self.grid = [[0 for x in range(size_y)] for y in range(size_x)]
        self.apple_pos_x = randint(0, size_x - 1)
        self.apple_pos_y = randint(0, size_y - 1)

        self.grid[self.apple_pos_x][self.apple_pos_y] = 1
        
        for case_x in range(0, self.size_y, margin):
            for case_y in range(0, self.size_x, margin):
                print(self.grid[case_x][case_y], end="")
                pygame.Rect(case_x, case_y, margin, margin)

            print("")


if __name__ == '__main__':
    
    size_x = 10
    size_y = 10
    margin = 20
    
    pygame.init()
    screen = pygame.display.set_mode((600, 600))

    grid = Grid(size_x, size_y, margin, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False