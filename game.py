from random import randint
import pygame, sys
from Snake import Snake

empty_cell_color = (255, 255, 255)
apple_cell_color = (255, 0, 0)
snakehead_cell_color = (0, 255, 255)
snakebody_cell_color = (0, 255, 0)


# Grid => 0 : Empty | 1 : Apple | 2 : Snake

class Grid:
    def __init__(self, num_rows, num_cols, screen):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.screen = screen

        self.apple_pos_x = randint(0, num_rows - 1)
        self.apple_pos_y = randint(0, num_cols - 1)

        self.grid_cell = [[]]


    def draw_grid(self):
        for x in range(self.num_rows):
            row = []
            for y in range(self.num_cols):
                rect = pygame.Rect(x * margin, y * margin, margin, margin)
                if x == self.apple_pos_x and y == self.apple_pos_y:
                    pygame.draw.rect(self.screen, apple_cell_color, rect)
                else:
                    pygame.draw.rect(self.screen, empty_cell_color, rect, 1)
                row.append(rect)
            self.grid_cell.append(row)
        
        self.snake = Snake(num_rows, num_cols)
        [snake_x, snake_y] = self.snake.getHead()
        head = self.grid_cell[snake_x][snake_y]
        pygame.draw.rect(self.screen, snakebody_cell_color, head, 0)

        pygame.display.update()

    def move_snake(self, key):
        if key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT:
            [head_x, head_y] = self.snake.getHead()
            apple = (pygame.K_UP and head_x - 1 == self.apple_pos_x) \
                or (pygame.K_DOWN and head_x + 1 == self.apple_pos_x) \
                or (pygame.K_LEFT and head_y - 1 == self.apple_pos_y) \
                or (pygame.K_RIGHT and head_y + 1 == self.apple_pos_y)
            alive, tail = self.snake.move(key, apple)
            if tail:
                # TODO: remove tail from drawn rectangles
                pass
            if not alive:
                # TODO: end game
                pass


if __name__ == '__main__':

    num_rows = 20
    num_cols = 20
    margin = 40
    WIDTH = num_rows * margin
    HEIGHT = num_cols * margin

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    grid = Grid(num_rows, num_cols, screen)

    running = True
    grid.draw_grid()
    while running:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
