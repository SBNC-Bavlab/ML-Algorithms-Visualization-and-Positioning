import tensorflow as tf
from bokeh.palettes import cividis

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

    def run_model(self, play_button, circles, lines):
        ''' generate and run the model '''
        batch_size = 128
        #display_step = 50
        loss_arr = []
        acc_arr = []
        progress_bar_length=10
        self.neural_nets()
        self.set_optimizers()
        cividis_colors = cividis(128)[55:87]
        cividis_colors += list(reversed(cividis_colors))
        cividis_colors = [item for item in cividis_colors for _ in range(4)]
        init = tf.global_variables_initializer()
        with tf.Session() as sess:

            sess.run(init)
            for step in range(1, self.epochs+1):
                batch_x, batch_y = mnist.train.next_batch(batch_size)
                sess.run(self.train_op, feed_dict={X: batch_x, Y: batch_y})
                loss, acc = sess.run([self.loss_op, self.accuracy], feed_dict={X: batch_x, Y: batch_y})

                '''
                if step % display_step == 0 or step == 1:
                    print("Step " + str(step) + ", Minibatch Loss= " + \
                          "{:.4f}".format(loss) + ", Training Accuracy= " + \
                          "{:.3f}".format(acc))
                '''
                lines.glyph.line_color = cividis_colors[step%256]
                circles.glyph.fill_color = circles.glyph.line_color = cividis_colors[step%256]
                text = "\r Bekleyiniz: [" + "+" * int(round(progress_bar_length * step/self.epochs))\
                       + '-' * (progress_bar_length - int(round(progress_bar_length * step/self.epochs)))\
                       + "] " + str(round(step/self.epochs * 100, 1)) + "%"
                play_button.label = text
                loss_arr.append(loss)
                acc_arr.append(acc)
            play_button.label = "Oynat"
            testing_acc = sess.run(self.accuracy, feed_dict={X: mnist.test.images, Y: mnist.test.labels})
        lines.glyph.line_color = "darkgray"
        circles.glyph.fill_color = circles.glyph.line_color = "lightseagreen"
        return testing_acc, loss_arr, acc_arr