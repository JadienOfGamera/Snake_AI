import numpy as np
import tensorflow as tf


class NN:
    def __init__(self, size_layers, activations):
        if len(size_layers) < 2:
            raise Exception("Not enough layers")
        if len(size_layers) != len(activations) + 1:
            raise Exception("Incompatible layer parameters array size: len(size_layers) must be equal to len(activations) + 1")

        self.size_layers = size_layers
        self.num_chromosomes = 0
        for i_size in range(len(size_layers) - 1):
            self.num_chromosomes += size_layers[i_size] * size_layers[i_size + 1]

        self.model = tf.keras.Sequential()

        self.model.add(tf.keras.Input(shape=size_layers[0]))
        for i_layer in range(len(activations)):
            self.model.add(
                tf.keras.layers.Dense(size_layers[i_layer + 1], activation=activations[i_layer], kernel_initializer=tf.keras.initializers.Zeros()))

    def set_weights(self, chromosomes):
        num_used_c = 0
        for layer_i in range(len(self.size_layers) - 1):
            weights = []
            for neuron_i in range(self.size_layers[layer_i]):
                weights.append(chromosomes[num_used_c + neuron_i * self.size_layers[layer_i + 1]: (num_used_c + neuron_i * self.size_layers[layer_i + 1] + self.size_layers[layer_i + 1])])
            bias = np.zeros(self.size_layers[layer_i + 1])
            self.model.layers[layer_i].set_weights([np.array(weights), bias])
            num_used_c += self.size_layers[layer_i] * self.size_layers[layer_i + 1]

    def predict(self, in_value):
        if len(in_value) != self.size_layers[0]:
            raise Exception("Invalid length of input array, size must be", self.size_layers[0])
        return self.model.predict(in_value)


if __name__ == "__main__":
    # INPUTS: manhattan distance head-apple, body length, free space on each side
    nn = NN([6, 9, 4], ["relu", "relu"])
    c = []
    for i in range(nn.num_chromosomes):
        c.append(i)
    print("LEN:", len(c))
    nn.set_weights(c)
    print(nn.model.weights)
