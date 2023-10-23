import random
import pygame


class Snake:
    def __init__(self, num_rows, num_cols):
        self.body = []
        self.body.append([random.randint(0, num_rows), random.randint(0, num_cols)])
        self.alive = True
        self.num_cols = num_cols
        self.num_rows = num_rows

    # key is a pygame.key
    def move(self, key, apple):
        match key:
            case pygame.K_UP:
                if self.body.__getitem__(0)[0] > 0 and not([[self.body.__getitem__(0)[0] - 1, self.body.__getitem__(0)[1]]] in self.body):
                    self.body.insert(0, [self.body.__getitem__(0)[0], self.body.__getitem__(0)[1]])
                else:
                    self.alive = False
            case pygame.K_DOWN:
                if self.body.__getitem__(0)[0] < self.num_rows and not([[self.body.__getitem__(0)[0] + 1, self.body.__getitem__(0)[1]]] in self.body):
                    self.body.insert(0, [self.body.__getitem__(0)[0], self.body.__getitem__(0)[1]])
                else:
                    self.alive = False
            case pygame.K_LEFT:
                if self.body.__getitem__(0)[1] > 0 and not ([[self.body.__getitem__(0)[0], self.body.__getitem__(0)[1] - 1]] in self.body):
                    self.body.insert(0, [self.body.__getitem__(0)[0], self.body.__getitem__(0)[1]])
                else:
                    self.alive = False
                pass
            case pygame.K_RIGHT:
                if self.body.__getitem__(0)[1] < self.num_cols and not ([[self.body.__getitem__(0)[0], self.body.__getitem__(0)[1] + 1]] in self.body):
                    self.body.insert(0, [self.body.__getitem__(0)[0], self.body.__getitem__(0)[1]])
                else:
                    self.alive = False
        if (key == pygame.K_UP or key == pygame.K_DOWN or key == pygame.K_LEFT or key == pygame.K_RIGHT) and not apple:
            self.body.pop()
        return self.alive
