import numpy as np

from neural_network import NN
from game import Game
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT


class SnakeNN(NN):
    def __init__(self):
        size_layers = [9, 10, 10,
                       4]  # We have chosen to have 4 layers of 9, 10, 10, 4 neurons. The first layout represents the 9 inputs described in game.py, when the last layout represents the 4 possible directions (up down left right)
        activations = ["tanh", "tanh",
                       "tanh"]  # Tanh activation allow us to provide negative numbers as inputs, and is very usefull performance-wise
        super().__init__(size_layers, activations)
        self.model.output_names = ["UP", "DOWN", "LEFT", "RIGHT"]

    # The genetic part of the code will generate a play to compute the fitness function of each agent, giving the score when the game is over.
    # Here are represented the 9 inputs
    def play(self, show=False):
        game = Game(show)
        alive = True
        score = 0
        snake_length = 1
        while alive:
            [ha_up, ha_down, ha_left, ha_right] = game.get_apple_distance() / np.linalg.norm(
                game.get_apple_distance())  # The 4 Manhattan distances
            [space_up, space_down, space_left, space_right] = game.get_free_space() / np.linalg.norm(
                game.get_free_space())  # The 4 free spaces at each direction
            output_nn = self.predict(
                [ha_up, ha_down, ha_left, ha_right, snake_length / 50, space_up, space_down, space_left, space_right])
            i_move = np.argmax(output_nn)
            moves = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
            alive, score = game.move_snake(moves[i_move])
            snake_length = score[0]  # Score
        return score
