import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf


class ActivationKernels:
    """show activation maps
    """
    def __init__(self, model):
        """init parameters 

        Args:
            model : base model 
        """

        self.model = model

        self.x, self.y = None, None  # training and testing dataset

    def load_data(self):
        """loat dataset of  CIFAR 10 
        """
        self.x, self.y = tf.keras.datasets.cifar10.load_data()

    def normalize_tensor(self, tensor):
        """normalize tensor

        Args:
            tensor (tensorflow.tensor): tensor before normalization

        Returns:
            tensor : tensor after normalization
        """
        return tf.divide(
            tf.subtract(tensor, tf.reduce_min(tensor)),
            tf.subtract(tf.reduce_max(tensor), tf.reduce_min(tensor)))

    def read_img(self, image_file, shape=(196, 196), plot=False):
        """read image from file and change datatype

        Args:
            image_file (str): image file 
            shape (tuple, optional): shape of image. Defaults to (196, 196).
            plot (bool, optional): whether plot the image after reading that. Defaults to False.
        Returns:
            image : tensorflow constant 
        """
        image = cv2.imread(image_file)

        image = cv2.resize(image[:, :, ::-1], shape)

        if plot:
            plt.imshow(image)

        image = tf.constant(image.reshape(1, *(shape), 3), dtype=tf.float32)

        return image

    def show_activations(self, image_file, layer, plot_image=False):
        """show kernels 

        Args:
            image_file (str): image file 
            layer (int): number of layer 
            plot_image (bool, optional): whether plot the image after reading that. Defaults to False.
        """
        # construct new model
        new_model = tf.keras.Sequential(self.model.layers[:layer + 1])
        # read image from file
        image = self.read_img(image_file, plot=plot_image)
        out = new_model(image)
        # get kernels
        kernels = self.model.layers[layer].get_weights()[0]
        kernels = kernels[:, :, :3, :]
        kernels = self.normalize_tensor(kernels)
        # plot
        fig, axs = plt.subplots(8, 8)
        index = 0
        for i in range(8):
            for j in range(4):

                ax_k = axs[i, j * 2]
                ax_k.set_xticks([])
                ax_k.set_yticks([])
                ax_k.imshow(kernels[:, :, :, index])

                ax_out = axs[i, j * 2 + 1]
                ax_out.set_xticks([])
                ax_out.set_yticks([])
                ax_out.imshow(out[0, :, :, index], cmap='plasma')

                index += 1

        fig.tight_layout()
        plt.subplots_adjust(wspace=0.005, hspace=0.05)
        fig.set_size_inches(8, 8)
