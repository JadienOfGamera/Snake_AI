import numpy as np

from neural_network import NN
from game import Game
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT


class SnakeNN(NN):
    def __init__(self):
        size_layers = [6, 9, 4]
        activations = ["relu", "relu"]
        super().__init__(size_layers, activations)
        self.model.output_names = ["UP", "DOWN", "LEFT", "RIGHT"]

    def play(self):
        game = Game()
        in_value = [0., 1., 30., 0.8, 0., 0.]
        alive = True
        score = 0
        while alive:
            output_nn = self.predict(in_value)
            i_move = np.argmax(output_nn)
            moves = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
            alive, score = game.move_snake(moves[i_move])
        return score
