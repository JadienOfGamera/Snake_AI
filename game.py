import time
from random import randint
import pygame, sys
from Snake import Snake

empty_cell_border_color = (255, 255, 255)
empty_cell_color = (0, 0, 0)
apple_cell_color = (255, 0, 0)
snake_cell_color = (0, 255, 0)

# Grid => 0 : Empty | 1 : Apple | 2 : Snake

class Grid:
    def __init__(self, num_rows, num_cols, screen):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.screen = screen
        self.apple_pos_x = None
        self.apple_pos_y = None

        self.snake = Snake(num_rows, num_cols)

        self.grid_cell = []
        self.draw_grid()

        self.generate_apple()

    def draw_grid(self):
        for x in range(self.num_rows):
            row = []
            for y in range(self.num_cols):
                rect = pygame.Rect(y * margin, x * margin, margin, margin)
                pygame.draw.rect(self.screen, empty_cell_border_color, rect, 1)
                row.append(rect)
            self.grid_cell.append(row)

        [snake_x, snake_y] = self.snake.getHead()
        head = self.grid_cell[snake_x][snake_y]
        pygame.draw.rect(self.screen, snake_cell_color, head, 0)
        pygame.display.update()

    def generate_apple(self):
        if self.apple_pos_x is not None and self.apple_pos_y is not None:
            oldAppleRect = self.grid_cell[self.apple_pos_x][self.apple_pos_y]
            pygame.draw.rect(self.screen, snake_cell_color, oldAppleRect)
            pygame.display.update(oldAppleRect)
        while self.apple_pos_x is None or self.apple_pos_y is None or [self.apple_pos_x, self.apple_pos_y] in self.snake.body:
            self.apple_pos_x = randint(0, num_rows - 1)
            self.apple_pos_y = randint(0, num_cols - 1)
        newAppleRect = self.grid_cell[self.apple_pos_x][self.apple_pos_y]
        pygame.draw.rect(self.screen, apple_cell_color, newAppleRect)
        pygame.display.update(newAppleRect)

    def move_snake(self, key):
        if key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT:
            [head_x, head_y] = self.snake.getHead()
            apple = (key == pygame.K_UP and head_x - 1 == self.apple_pos_x and head_y == self.apple_pos_y) \
                or (key == pygame.K_DOWN and head_x + 1 == self.apple_pos_x and head_y == self.apple_pos_y) \
                or (key == pygame.K_LEFT and head_y - 1 == self.apple_pos_y and head_x == self.apple_pos_x) \
                or (key == pygame.K_RIGHT and head_y + 1 == self.apple_pos_y and head_x == self.apple_pos_x)
            alive, tail = self.snake.move(key, apple)  # apple
            if not (tail is None):
                tailRect = self.grid_cell[tail[0]][tail[1]]
                pygame.draw.rect(self.screen, empty_cell_color, tailRect)
                pygame.draw.rect(self.screen, empty_cell_border_color, tailRect, 1)
                pygame.display.update(tailRect)
            if apple:
                self.generate_apple()
            if alive:
                [head_x, head_y] = self.snake.getHead()
                headRect = self.grid_cell[head_x][head_y]
                pygame.draw.rect(self.screen, snake_cell_color, headRect)
                pygame.display.update(headRect)
            else:
                print(len(self.snake.body))
                pygame.display.quit()
                pass


def start():

    grid = Grid(num_rows, num_cols, screen)
    running = True

    while running:
        for event in pygame.event.get():
            pygame.event.set_blocked(pygame.KEYDOWN)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                grid.move_snake(event.key)
            pygame.event.clear()
            pygame.event.set_allowed(pygame.KEYDOWN)


if __name__ == '__main__':
    num_rows = 20
    num_cols = 20
    margin = 40
    WIDTH = num_rows * margin
    HEIGHT = num_cols * margin

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start()
