import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)


# tf placeholders
X = tf.placeholder("float", [None, 784])
Y = tf.placeholder("float", [None, 10])


class Ann(object):
    ''' class '''
    def __init__(self, learning_rate, activation_function, layers, epochs):
        self.num_input = 784
        self.num_classes = 10
        self.learning_rate = learning_rate
        self.activation_function = activation_function
        self.layers = layers
        self.epochs = epochs
        self.logits = None
        self.prediction = None
        self.loss_op = None
        self.train_op = None
        self.accuracy = None
        self.correct_pred = None

    def neural_nets(self):
        ''' Set neural nets and connect them '''
        layers = []
        if self.activation_function == "ReLu":
            for i, _ in enumerate(self.layers):
                if i == 0:
                    if i+1 != len(self.layers):
                        layers.append(
                            tf.nn.relu(
                                tf.add(tf.matmul(X, tf.Variable(tf.random_normal([self.num_input,
                                                                                  self.layers[i]]))),
                                       tf.Variable(tf.random_normal([self.layers[i]])))
                            )
                        )
                        layers.append(
                            tf.nn.relu(
                                tf.add(tf.matmul(layers[-1], tf.Variable(tf.random_normal([self.layers[i],
                                                                                           self.layers[i+1]]))),
                                       tf.Variable(tf.random_normal([self.layers[i+1]])))
                            )
                        )
                    else:
                        layers.append(
                            tf.nn.relu(
                                tf.add(tf.matmul(X, tf.Variable(tf.random_normal([self.num_input,
                                                                                  self.layers[i]]))),
                                       tf.Variable(tf.random_normal([self.layers[i]])))
                            )
                        )
                        layers.append(
                            tf.add(tf.matmul(layers[-1],
                                             tf.Variable(tf.random_normal([self.layers[i],
                                                                           self.num_classes]))),
                                   tf.Variable(tf.random_normal([self.num_classes])))
                        )
                        self.logits = layers[-1]
                        self.prediction = tf.nn.softmax(self.logits)
                elif i+1 == len(self.layers):
                    layers.append(
                        tf.add(tf.matmul(layers[-1],
                                         tf.Variable(tf.random_normal([self.layers[i],
                                                                       self.num_classes]))),
                               tf.Variable(tf.random_normal([self.num_classes])))
                    )
                    self.logits = layers[-1]
                    self.prediction = tf.nn.softmax(self.logits)
                else:
                    layers.append(
                        tf.nn.relu(
                            tf.add(tf.matmul(layers[-1], tf.Variable(tf.random_normal([self.layers[i],
                                                                                       self.layers[i+1]]))),
                                   tf.Variable(tf.random_normal([self.layers[i+1]])))
                        )
                    )

        elif self.activation_function == "Sigmoid":
            for i, _ in enumerate(self.layers):
                if i == 0:
                    if i+1 != len(self.layers):
                        layers.append(
                            tf.nn.sigmoid(
                                tf.add(tf.matmul(X, tf.Variable(tf.random_normal([self.num_input,
                                                                                  self.layers[i]]))),
                                       tf.Variable(tf.random_normal([self.layers[i]])))
                            )
                        )
                        layers.append(
                            tf.nn.sigmoid(
                                tf.add(tf.matmul(layers[-1], tf.Variable(tf.random_normal([self.layers[i],
                                                                                           self.layers[i+1]]))),
                                       tf.Variable(tf.random_normal([self.layers[i+1]])))
                            )
                        )
                    else:
                        layers.append(
                            tf.nn.sigmoid(
                                tf.add(tf.matmul(X, tf.Variable(tf.random_normal([self.num_input,
                                                                                  self.layers[i]]))),
                                       tf.Variable(tf.random_normal([self.layers[i]])))
                            )
                        )
                        layers.append(
                            tf.add(tf.matmul(layers[-1],
                                             tf.Variable(tf.random_normal([self.layers[i],
                                                                           self.num_classes]))),
                                   tf.Variable(tf.random_normal([self.num_classes])))
                        )
                        self.logits = layers[-1]
                        self.prediction = tf.nn.softmax(self.logits)
                elif i+1 == len(self.layers):
                    layers.append(
                        tf.add(tf.matmul(layers[-1],
                                         tf.Variable(tf.random_normal([self.layers[i],
                                                                       self.num_classes]))),
                               tf.Variable(tf.random_normal([self.num_classes])))
                    )
                    self.logits = layers[-1]
                    self.prediction = tf.nn.softmax(self.logits)
                else:
                    layers.append(
                        tf.nn.sigmoid(
                            tf.add(tf.matmul(layers[-1], tf.Variable(tf.random_normal([self.layers[i],
                                                                                       self.layers[i+1]]))),
                                   tf.Variable(tf.random_normal([self.layers[i+1]])))
                        )
                    )
        elif self.activation_function == "Tanh":
            for i, _ in enumerate(self.layers):
                if i == 0:
                    if i+1 != len(self.layers):
                        layers.append(
                            tf.nn.tanh(
                                tf.add(tf.matmul(X, tf.Variable(tf.random_normal([self.num_input,
                                                                                  self.layers[i]]))),
                                       tf.Variable(tf.random_normal([self.layers[i]])))
                            )
                        )
                        layers.append(
                            tf.nn.tanh(
                                tf.add(tf.matmul(layers[-1], tf.Variable(tf.random_normal([self.layers[i],
                                                                                           self.layers[i+1]]))),
                                       tf.Variable(tf.random_normal([self.layers[i+1]])))
                            )
                        )
                    else:
                        layers.append(
                            tf.nn.tanh(
                                tf.add(tf.matmul(X, tf.Variable(tf.random_normal([self.num_input,
                                                                                  self.layers[i]]))),
                                       tf.Variable(tf.random_normal([self.layers[i]])))
                            )
                        )
                        layers.append(
                            tf.add(tf.matmul(layers[-1],
                                             tf.Variable(tf.random_normal([self.layers[i],
                                                                           self.num_classes]))),
                                   tf.Variable(tf.random_normal([self.num_classes])))
                        )
                        self.logits = layers[-1]
                        self.prediction = tf.nn.softmax(self.logits)
                elif i+1 == len(self.layers):
                    layers.append(
                        tf.add(tf.matmul(layers[-1],
                                         tf.Variable(tf.random_normal([self.layers[i],
                                                                       self.num_classes]))),
                               tf.Variable(tf.random_normal([self.num_classes])))
                    )
                    self.logits = layers[-1]
                    self.prediction = tf.nn.softmax(self.logits)
                else:
                    layers.append(
                        tf.nn.tanh(
                            tf.add(tf.matmul(layers[-1], tf.Variable(tf.random_normal([self.layers[i],
                                                                                       self.layers[i+1]]))),
                                   tf.Variable(tf.random_normal([self.layers[i+1]])))
                        )
                    )

    def set_optimizers(self):
        ''' Set optimizer and models variables'''
        self.loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.logits, labels=Y))
        optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate)
        self.train_op = optimizer.minimize(self.loss_op)
        self.correct_pred = tf.equal(tf.argmax(self.prediction, 1), tf.argmax(Y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(self.correct_pred, tf.float32))

    def run_model(self):
        ''' generate and run the model '''
        batch_size = 128
        display_step = 100
        loss_arr = []
        acc_arr = []

        self.neural_nets()
        self.set_optimizers()

        init = tf.global_variables_initializer()

        with tf.Session() as sess:

            sess.run(init)

            for step in range(1, self.epochs+1):
                batch_x, batch_y = mnist.train.next_batch(batch_size)
                sess.run(self.train_op, feed_dict={X: batch_x, Y: batch_y})
                loss, acc = sess.run([self.loss_op, self.accuracy], feed_dict={X: batch_x, Y: batch_y})
                if step % display_step == 0 or step == 1:
                    print("Step " + str(step) + ", Minibatch Loss= " + \
                          "{:.4f}".format(loss) + ", Training Accuracy= " + \
                          "{:.3f}".format(acc))
                loss_arr.append(loss)
                acc_arr.append(acc)
            testing_acc = sess.run(self.accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels})

            print(testing_acc)
        graph_plot(self.epochs, loss_arr, "LOSS")
        graph_plot(self.epochs, acc_arr, "ACC")


def graph_plot(num_epoch, _loss_arr, title):
    ''' plot loss or acc graph '''
    # Plots the loss array
    plt.plot(np.arange(num_epoch), _loss_arr, label='train')
    plt.legend(loc='upper right')
    plt.title(title)
    plt.show()


# ann = Ann(0.01, "ReLu", [500, 500, 500], 5000)
# ann.run_model()
