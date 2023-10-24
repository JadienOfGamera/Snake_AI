import random
import pygame


class Snake:
    def __init__(self, num_rows, num_cols):
        self.body = []
        self.body.append([random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)])
        self.alive = True
        self.num_cols = num_cols
        self.num_rows = num_rows

    # key is a pygame.key
    def move(self, key, apple):
        match key:
            case pygame.K_UP:
                if self.body[0][0] > 0 and not([self.body[0][0] - 1, self.body[0][1]] in self.body):
                    self.body.insert(0, [self.body[0][0] - 1, self.body[0][1]])
                else:
                    self.alive = False
            case pygame.K_DOWN:
                if self.body[0][0] < self.num_rows - 1 and not([self.body[0][0] + 1, self.body[0][1]] in self.body):
                    self.body.insert(0, [self.body[0][0] + 1, self.body[0][1]])
                else:
                    self.alive = False
            case pygame.K_LEFT:
                if self.body[0][1] > 0 and not ([self.body[0][0], self.body[0][1] - 1] in self.body):
                    self.body.insert(0, [self.body[0][0], self.body[0][1] - 1])
                else:
                    self.alive = False
                pass
            case pygame.K_RIGHT:
                if self.body[0][1] < self.num_cols - 1 and not ([self.body[0][0], self.body[0][1] + 1] in self.body):
                    self.body.insert(0, [self.body[0][0], self.body[0][1] + 1])
                else:
                    self.alive = False
        tail = None
        if not apple: # (key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT) and
            tail = self.body.pop()
        return self.alive, tail

    def getHead(self):
        return self.body[0]
