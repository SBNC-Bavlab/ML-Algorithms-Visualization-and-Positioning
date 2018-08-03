"""
Class for storing ANN data
"""


class ANNData():
    def __init__(self, learning_rate, activation_func, layers, epoch):
        self.learning_rate = learning_rate
        self.activation_func = activation_func
        self.layers = layers
        self.epoch = epoch

    def update(self, learning_rate, activation_func, layers, epoch):
        self.learning_rate = learning_rate
        self.activation_func = activation_func
        self.layers = layers
        self.epoch = epoch