import random
import pygame


# The Snake object is the changing part of the software. A Snake possess a Head (with coordinates within the grid), and a Body/Tail (list of coordinates within the grid which follows the Head)
# The Body itself increases when the Head as the same coordinates as an apple, adding an element ((X, Y) => corresponding to self.last_move) to the self.body list
class Snake:
    def __init__(self, num_rows, num_cols):
        self.body = []
        self.body.append([random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)])
        self.alive = True
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.last_move = None

    # key is a pygame.key
    def move(self, key, apple):
        # At each movement we verify if the snake's head is still within the grid. Otherwise, it means that the party's over, and the snake is dead
        match key:
            case pygame.K_UP:
                if self.body[0][0] > 0 and not ([self.body[0][0] - 1, self.body[0][1]] in self.body) and not (
                        self.last_move == pygame.K_DOWN):
                    self.body.insert(0, [self.body[0][0] - 1, self.body[0][1]])
                    self.last_move = pygame.K_UP
                else:
                    self.alive = False
            case pygame.K_DOWN:
                if self.body[0][0] < self.num_rows - 1 and not (
                        [self.body[0][0] + 1, self.body[0][1]] in self.body) and not (self.last_move == pygame.K_UP):
                    self.body.insert(0, [self.body[0][0] + 1, self.body[0][1]])
                    self.last_move = pygame.K_DOWN
                else:
                    self.alive = False
            case pygame.K_LEFT:
                if self.body[0][1] > 0 and not ([self.body[0][0], self.body[0][1] - 1] in self.body) and not (
                        self.last_move == pygame.K_RIGHT):
                    self.body.insert(0, [self.body[0][0], self.body[0][1] - 1])
                    self.last_move = pygame.K_LEFT
                else:
                    self.alive = False
            case pygame.K_RIGHT:
                if self.body[0][1] < self.num_cols - 1 and not (
                        [self.body[0][0], self.body[0][1] + 1] in self.body) and not (self.last_move == pygame.K_LEFT):
                    self.body.insert(0, [self.body[0][0], self.body[0][1] + 1])
                    self.last_move = pygame.K_RIGHT
                else:
                    self.alive = False
        tail = None
        if not apple:
            tail = self.body.pop()
        return self.alive, tail

    def getHead(self):
        return self.body[0]
