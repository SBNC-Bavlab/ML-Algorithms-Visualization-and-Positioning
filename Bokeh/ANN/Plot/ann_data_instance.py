"""
Class for storing ANN data
"""


class ANNData():
    def __init__(self, learning_rate, activation_func, layers):
        self.learning_rate = learning_rate
        self.activation_func = activation_func
        self.layers = layers

    def update(self, learning_rate, activation_func, layers):
        self.learning_rate = learning_rate
        self.activation_func = activation_func
        self.layers = layers
