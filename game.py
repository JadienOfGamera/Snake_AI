import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from random import randint
import pygame
from Snake import Snake

empty_cell_border_color = (255, 255, 255)
empty_cell_color = (0, 0, 0)
apple_cell_color = (255, 0, 0)
snake_cell_color = (0, 255, 0)
margin = 40

NUM_ROWS = 10
NUM_COLS = 10
MAX_MOVES_NO_APPLE = 50


class Game:
    def __init__(self, show=True):
        self.show = show
        if self.show:
            pygame.init()
            screen = pygame.display.set_mode((NUM_COLS * margin, NUM_ROWS * margin))  # (width, height)
            self.screen = screen

        self.num_rows = NUM_ROWS
        self.num_cols = NUM_COLS
        self.apple_pos_x = None
        self.apple_pos_y = None

        self.snake = Snake(self.num_rows, self.num_cols)

        self.grid_data = [ [0] * self.num_cols for _ in range(self.num_rows)]
        self.grid_cell = []
        self.draw_grid()

        self.generate_apple()
        self.moves_no_apple = 0
        self.num_moves = 0

    def draw_grid(self):
        if self.show:
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
        if self.apple_pos_x is not None and self.apple_pos_y is not None and self.show:
            oldAppleRect = self.grid_cell[self.apple_pos_x][self.apple_pos_y]
            pygame.draw.rect(self.screen, snake_cell_color, oldAppleRect)
            pygame.display.update(oldAppleRect)
        while self.apple_pos_x is None or self.apple_pos_y is None or [self.apple_pos_x, self.apple_pos_y] in self.snake.body:
            self.apple_pos_x = randint(0, self.num_rows - 1)
            self.apple_pos_y = randint(0, self.num_cols - 1)
        if self.show:
            newAppleRect = self.grid_cell[self.apple_pos_x][self.apple_pos_y]
            pygame.draw.rect(self.screen, apple_cell_color, newAppleRect)
            pygame.display.update(newAppleRect)
        self.grid_data[self.apple_pos_x][self.apple_pos_y] = 0

    def move_snake(self, key):
        if key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.moves_no_apple += 1
            self.num_moves += 1
            [head_x, head_y] = self.snake.getHead()
            apple = (key == pygame.K_UP and head_x - 1 == self.apple_pos_x and head_y == self.apple_pos_y) \
                or (key == pygame.K_DOWN and head_x + 1 == self.apple_pos_x and head_y == self.apple_pos_y) \
                or (key == pygame.K_LEFT and head_y - 1 == self.apple_pos_y and head_x == self.apple_pos_x) \
                or (key == pygame.K_RIGHT and head_y + 1 == self.apple_pos_y and head_x == self.apple_pos_x)
            alive, tail = self.snake.move(key, apple)  # apple
            if not (tail is None) and self.show:
                tailRect = self.grid_cell[tail[0]][tail[1]]
                if self.show:
                    pygame.draw.rect(self.screen, empty_cell_color, tailRect)
                    pygame.draw.rect(self.screen, empty_cell_border_color, tailRect, 1)
                    pygame.display.update(tailRect)
            if apple:
                self.generate_apple()
                self.moves_no_apple = 0
            if alive and not(self.moves_no_apple > MAX_MOVES_NO_APPLE):
                if self.show:
                    [head_x, head_y] = self.snake.getHead()
                    headRect = self.grid_cell[head_x][head_y]
                    pygame.draw.rect(self.screen, snake_cell_color, headRect)
                    pygame.display.update(headRect)
                return True, self.get_score()
            else:
                pygame.display.quit()
                return False, self.get_score()

    def get_score(self):
        return len(self.snake.body), self.num_moves

    def get_free_space(self):
        [space_up, space_down, space_left, space_right] = [0, 0, 0, 0]

        head_x, head_y = self.snake.getHead()
        
        # Up
        for i in range(1, self.num_cols):
            new_x, new_y = head_x - i, head_y
            if new_x < 0 or self.grid_data[new_x][new_y] != 0 or [new_x, new_y] in self.snake.body:
                break
            space_up += 1

        # Down
        for i in range(1, self.num_cols):
            new_x, new_y = head_x + i, head_y
            if new_x >= self.num_cols or self.grid_data[new_x][new_y] != 0 or [new_x, new_y] in self.snake.body:
                break
            space_down += 1

        # Right
        for i in range(1, self.num_rows):
            new_x, new_y = head_x, head_y + i
            if new_y >= self.num_rows or self.grid_data[new_x][new_y] != 0 or [new_x, new_y] in self.snake.body:
                break
            space_right += 1

        # Left
        for i in range(1, self.num_rows):
            new_x, new_y = head_x, head_y - i
            if new_y < 0 or self.grid_data[new_x][new_y] != 0 or [new_x, new_y] in self.snake.body:
                break
            space_left += 1

        return [space_up, space_down, space_left, space_right]

    def get_apple_distance(self):
        md_up = abs(self.apple_pos_x - self.snake.getHead()[0]) + abs(self.apple_pos_y - (self.snake.getHead()[1] - 1))
        md_down = abs(self.apple_pos_x - self.snake.getHead()[0]) + abs(self.apple_pos_y - (self.snake.getHead()[1] + 1))
        md_left = abs(self.apple_pos_x - (self.snake.getHead()[0] - 1)) + abs(self.apple_pos_y - self.snake.getHead()[1])
        md_right = abs(self.apple_pos_x - (self.snake.getHead()[0] + 1)) + abs(self.apple_pos_y - self.snake.getHead()[1])
        return [md_up, md_down, md_left, md_right]

    def start_human(self):
        running = True
        score = 0

        while running:
            for event in pygame.event.get():
                pygame.event.set_blocked(pygame.KEYDOWN)
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running, score = self.move_snake(event.key)
                if running:
                    pygame.event.clear()
                    pygame.event.set_allowed(pygame.KEYDOWN)

        print("Final score:", score)


if __name__ == '__main__':
    game = Game()
    game.start_human()
