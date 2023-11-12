import numpy as np
import tensorflow as tf


class NN:
    def __init__(self, size_layers, activations):
        if len(size_layers) < 2:
            raise Exception("Not enough layers")
        if len(size_layers) != len(activations) + 1:
            raise Exception("Incompatible layer parameters array size: len(size_layers) must be equal to len("
                            "activations) + 1")

        self.size_layers = size_layers
        self.num_chromosomes = 0
        for i_size in range(len(size_layers) - 1):
            self.num_chromosomes += (size_layers[i_size] * 2 * size_layers[i_size + 1])

        self.model = tf.keras.Sequential()

        self.model.add(tf.keras.Input(shape=size_layers[0]))
        for i_layer in range(len(activations)):
            self.model.add(
                tf.keras.layers.Dense(size_layers[i_layer + 1], activation=activations[i_layer], kernel_initializer=tf.keras.initializers.Zeros(), name=("Dense" + str(i_layer))))

    def set_weights(self, chromosomes):
        for layer_i in range(len(self.size_layers) - 1):
            weights = []
            bias = np.array([])
            c_used = 0
            for neuron_i in range(self.size_layers[layer_i]):
                # Considering all neurons to be numbered sequentially we consider the agent to be [w1 b1 w2 b2 ... ]
                weights.append(chromosomes[c_used : c_used + self.size_layers[layer_i + 1]])
                c_used += self.size_layers[layer_i + 1]
            bias = np.append(bias, chromosomes[c_used : c_used + self.size_layers[layer_i + 1]])
            c_used += self.size_layers[layer_i + 1]
            self.model.layers[layer_i].set_weights([np.array(weights), bias])

    def predict(self, in_value):
        if len(in_value) != self.size_layers[0]:
            raise Exception("Invalid length of input array, size must be", self.size_layers[0])
        return self.model.predict(tf.keras.utils.normalize(in_value, axis=0), verbose=0)


if __name__ == "__main__":
    # INPUTS: manhattan distance head-apple, body length, free space on each side
    nn = NN([6, 9, 4], ["relu", "relu"])
    c = []
    for i in range(nn.num_chromosomes):
        c.append(i)
    print("LEN:", len(c))
    nn.set_weights(c)
    print(nn.model.weights)
    print(nn.predict([0, 1, 0.2, 0.3, 0, 1]))
