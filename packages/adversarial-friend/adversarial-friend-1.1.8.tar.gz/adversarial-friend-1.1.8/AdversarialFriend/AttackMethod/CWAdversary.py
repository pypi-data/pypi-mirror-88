from .Adversary import Adversary

import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.applications import MobileNet
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.mobilenet import preprocess_input  # may change


class CWAdversary(Adversary):
    """C&W Adversial Attacking Methodd """
    def __init__(self, model, max_iter=2, lr=0.1, c=1e2, k=0):
        """init parameters 

        Args:
            model ([type]): tensorflow model 
            max_iter (int, optional): maximum number of iterations. Defaults to 2.
            lr (float, optional): learning rate. Defaults to 0.1.
            c ([type], optional): [description]. Defaults to 1e2.
            k (int, optional): [description]. Defaults to 0.
        """
        super().__init__()
        self.model = model
        self.max_iter = max_iter
        self.lr = lr
        self.clip = 1
        self.c = c
        self.k = k

    def attack(self, T, verbose=False):
        """attack method

        Args:
            T ([type]): target class 
            verbose (bool, optional): verbose mode. Defaults to False.
        """
        opt = tf.keras.optimizers.Adam(lr=self.lr)

        X = self.image.reshape(1, *self.image.shape)

        x = X.copy()  # assuming numpy array

        x = tf.constant(x, dtype=tf.float32)

        w = tf.Variable(np.zeros(X.shape), dtype=tf.float32)

        Z = tf.keras.Sequential(self.model.layers[:-1])  # logits

        # square the constraint?
        f = lambda : tf.linalg.norm(0.5 * (tf.tanh(w) + 1.0) - x, ord=2) + \
                     self.c * tf.math.maximum(
                     tf.math.reduce_max(Z(0.5 * (tf.tanh(w) + 1.0))) -\
                     Z(0.5 * (tf.tanh(w) + 1.0)), -self.k)

        for i in range(self.max_iter):

            opt.minimize(f, var_list=[w])

        self.attack_image = 0.5 * (tf.tanh(w) + 1)

        # print("DIFF IMGAGE:")
        diff = self.show_diff()
        return self.pred_attack(), diff
