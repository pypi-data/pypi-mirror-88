import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.applications import MobileNet
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.mobilenet import preprocess_input  # may change


class CNN_feat_visualizer:
    """CNN Visualizer
    """
    def __init__(self, max_iter=2048, lr=0.1, clip=1):
        """init parameters

        Args:
            max_iter (int, optional): number of max iter. Defaults to 2048.
            lr (float, optional): learning rate. Defaults to 0.1.
            clip (int, optional): clip. Defaults to 1.
        """
        self.max_iter = max_iter
        self.lr = lr
        self.clip = 1

    def fit(self, model, layer=3, node=None, verbose=False):
        """Main function

        Args:
            model : tensorflow model
            layer (int, optional): layer of model. Defaults to 3.
            node ([type], optional): node. Defaults to None.
            verbose (bool, optional): verbose. Defaults to False.

        Returns:
            tensor after computation
        """
        input_shape = model.input_shape
        input_shape = tuple([1]) + input_shape[1:]
        p = 2 if node == None else 1  # choose DeepDream objective is node set to None
        X = np.random.normal(size=input_shape)

        submodel = tf.keras.Sequential(model.layers[:layer])

        for i in range(self.max_iter):
            X = self.step(X, submodel, node, p)
        return X

    def step(self, x, submodel, node, p):
        '''
    TO-DO: Add regularization. Examples not clean
    Things to try:
    - Blur image inbetween iterations
    - Add pixel local frequency regularization?
    '''

        x = tf.Variable(x)
        with tf.GradientTape() as tape:
            out = submodel(x)[0, :, :, node]
            f = tf.linalg.norm(out, ord=2)**p
        dfdx = tape.gradient(f, x)
        new_image = x + self.lr * tf.sign(dfdx)
        new_image = tf.clip_by_value(new_image, -self.clip, self.clip)
        return new_image.numpy()