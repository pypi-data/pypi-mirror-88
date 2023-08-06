import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from mpl_toolkits.axes_grid1 import ImageGrid


class LogisticRegression:
    """create simple LogisticRegression model"""
    def __init__(self):
        """init parameters"""

        self.model = tf.keras.Sequential()

        self.class_labels = []

        self.x_train, self.y_train = None, None

        self.x_valid, self.y_valid = None, None

    def load_data(self, class_labels):
        """load CIFAR 10 data set

        Args:
            class_labels (list): class labels for data set  
        """
        # use test as validation since no need to holdout
        (self.x_train,
         self.y_train), (self.x_valid,
                         self.y_valid) = tf.keras.datasets.cifar10.load_data()

        self.class_labels = class_labels

    def fit(self,
            epochs=150,
            input_shape=[32, 32, 3],
            units=10,
            activation='softmax',
            use_bias=False,
            loss="sparse_categorical_crossentropy",
            optimizer="sgd",
            metrics=["accuracy"],
            verbose=0):
        """
        fit model 

        Args:
            epochs (int): Number of epochs to train the model. Defaults to 150.
            input_shape (list, optional): Input shape. Defaults to [32, 32, 3].
            units (int, optional): Positive integer, dimensionality of the output space. Defaults to 10.
            activation (str, optional): Activation function to use. Defaults to 'softmax'.
            use_bias (bool, optional): whether the layer uses a bias vector Defaults to False.
            loss (str, optional):name of objective function. Defaults to "sparse_categorical_crossentropy".
            optimizer (str, optional): optimizer instance. Defaults to "sgd".
            metrics (list, optional): List of metrics to be evaluated by the model during training and testing. Defaults to ["accuracy"].
            verbose (int, optional): Verbosity mode. Defaults to 0.
        """

        self.model.add(tf.keras.layers.Flatten(input_shape=input_shape))

        self.model.add(
            tf.keras.layers.Dense(units,
                                  activation=activation,
                                  use_bias=use_bias))

        self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)

        history = self.model.fit(self.x_train,
                                 self.y_train,
                                 epochs=epochs,
                                 verbose=verbose,
                                 batch_size=len(self.x_train),
                                 validation_data=(self.x_valid, self.y_valid))

    def show_feature_maps(self, layer_id=0, input_shape=[32, 32, 3]):
        """plot feature maps

        Args:
            class_labels (list, optional): class labels of data set. Defaults to None.
            layer_id (int, optional): layer id. Defaults to 0.
            input_shape (list, optional): input shape. Defaults to [32, 32, 3].
        """

        layer = self.model.weights[layer_id]

        N, K = layer.shape

        fig = plt.figure(figsize=(20., 20.))

        grid = ImageGrid(fig, 111, nrows_ncols=(2, 5), axes_pad=0.4)

        for ax, k in zip(grid, range(K)):
            image = tf.reshape(layer[:, k], input_shape)
            ax.imshow(image)
            if self.class_labels:
                ax.set_title(self.class_labels[k])

    def compute_gradient(self, number=3, target_class=1, shape=[32, 32, 3]):
        """compuate gradient and plot featrue map for one class

        Args:
            number (int, optional): number for computing gradient. Defaults to 3.
            target_class (int, optional): target class of data set . Defaults to 1.
            shape (list, optional): input shape. Defaults to [32, 32, 3].
        """

        input_shape = [1, *shape]

        dummy_input = tf.Variable(np.zeros(shape=input_shape))  # blank vector

        with tf.GradientTape() as tape:
            dummy_output = self.model(dummy_input)
            loss = tf.keras.losses.sparse_categorical_crossentropy(
                target_class, dummy_output)

        grads = tape.gradient(loss, dummy_input)

        reshaped_grads = tf.reshape(grads, shape)

        scaled_grads = np.zeros(tuple(shape))

        for k in range(number):

            mini = np.min(reshaped_grads[:, :, k])

            maxi = np.max(reshaped_grads[:, :, k])

            scale = maxi - mini

            scaled_grads[:, :, k] = (reshaped_grads[:, :, k] - mini) / scale

        plt.title(
            f"Computed gradient to maximize class {self.class_labels[target_class]} "
        )

        plt.imshow(scaled_grads)
