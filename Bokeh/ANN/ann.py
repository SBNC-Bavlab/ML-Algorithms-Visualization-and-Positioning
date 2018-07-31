import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import pickle
bank = pickle.load(open('bank.pkl', 'rb'))
x_train = bank['x_train']
y_train = bank['y_train']
x_test = bank['x_test']
y_test = bank['y_test']

# Parameters
learning_rate = 0.01
epochs = 2000
hidden1 = 3
inputs = 4
classes = 2

# tf placeholders
X = tf.placeholder("float", [None, 4])
Y = tf.placeholder("float", [None, 2])


def graph_plot(num_epoch, _loss_arr):
    """ plot the results"""
    # Plots the loss array
    plt.plot(np.arange(num_epoch), _loss_arr, label='train')
    plt.legend(loc='upper right')
    plt.show()


# ANN class
class AnnHidden1:
    """ Ann class"""
    # Initializer
    def __init__(self, hidden_unit1, input_unit, classes_unit):
        self.hidden1 = tf.Variable(tf.random_normal([input_unit, hidden_unit1]))
        self.hidden_out = tf.Variable(tf.random_normal([hidden_unit1, classes_unit]))
        self.bias1 = tf.Variable(tf.random_normal([hidden_unit1]))
        self.bias_out = tf.Variable(tf.random_normal([classes_unit]))
        self.model = None
        self.loss_opt = None
        self.train_opt = None
        self.accuracy = None

    # set layers
    def set_model(self, x):
        """ attach layers """
        layer1 = tf.nn.relu(tf.add(tf.matmul(x, self.hidden1), self.bias1))
        out_layer = tf.matmul(layer1, self.hidden_out) + self.bias_out
        self.model = tf.nn.softmax(out_layer)

    # set loss and accuracy
    def loss_acc(self, rate, y):
        """ loss graph """
        self.loss_opt = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.model, labels=y))
        self.train_opt = tf.train.GradientDescentOptimizer(learning_rate=rate).minimize(self.loss_opt)
        prediction_opt = tf.equal(tf.argmax(self.model, 1), tf.argmax(y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(prediction_opt, tf.float32))


if __name__ == "__main__":

    loss_arr = []

    model = AnnHidden1(hidden1, inputs, classes)
    model.set_model(X)
    model.loss_acc(learning_rate, Y)

    init = tf.global_variables_initializer()

    with tf.Session() as sess:

        sess.run(init)

        for epoch in range(1, epochs+1):
            loss, acc, _ = sess.run([model.loss_opt, model.accuracy, model.train_opt], feed_dict={X: x_train, Y: y_train})
            print("Epoch: " + str(epoch) + " Loss: " + "{:.4f}".format(loss))
            loss_arr.append(loss)

        print("Testing Accuracy: ", sess.run(model.accuracy, feed_dict={X: x_test, Y: y_test}))

    graph_plot(epochs, loss_arr)
