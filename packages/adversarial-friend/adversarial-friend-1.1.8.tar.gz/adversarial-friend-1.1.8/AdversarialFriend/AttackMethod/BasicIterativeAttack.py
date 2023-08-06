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


class BasicIterativeAttack(Adversary):
    """basic interative attack  
    """
    def __init__(self, model, max_iter=50, lr=0.1, clip=1):
        """init parameters

        Args:
            model : tensorflow model 
            max_iter (int, optional): maximum number of iteration. Defaults to 50.
            lr (float, optional): learning rate. Defaults to 0.1.
            clip (int, optional): clip parameter. Defaults to 1.
        """
        super().__init__()
        self.max_iter = max_iter
        self.lr = lr
        self.clip = 1
        self.model = model

    def step(self, X, y, loss):
        """compute gradient

        Args:
            X : attacking image array 
            y  : target class
            loss : loss function  

        Returns:
            new image array after computation 
        """
        x = tf.Variable(X)
        y = tf.constant(y)
        with tf.GradientTape() as tape:
            L = loss(y, self.model(x))
        dLdx = tape.gradient(L, x)
        new_image = x - self.lr * tf.sign(dLdx)
        new_image = tf.clip_by_value(new_image, -self.clip, self.clip)
        return new_image.numpy()

    def attack(self,
               target,
               loss=tf.keras.losses.CategoricalCrossentropy(),
               verbose=False):
        """attack method

        Args:
            target : target class    
            loss  : loss function. Defaults to tf.keras.losses.CategoricalCrossentropy().
            verbose : Verbose mode. Defaults to False.

        Raises:
            SystemExit: check if read image 

        Returns:
            pred_attack: prediction for attack image 
            diff : distance between original image and attack image

        """
        if not isinstance(self.image, np.ndarray):
            raise SystemExit("PLEASE READ IMAGE!!")

        cat_in = self.image.reshape(1, *self.image.shape)

        self.attack_image = cat_in.copy()  # assuming numpy array
        # begin to attack
        for i in range(self.max_iter):
            self.attack_image = self.step(self.attack_image, target, loss)

        # print("DIFF IMGAGE:")
        diff = self.show_diff()
        return self.pred_attack(), diff
