import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.applications import MobileNet
from keras.applications.imagenet_utils import decode_predictions
from keras.applications.mobilenet import preprocess_input  # may change


class Adversary:
    def __init__(self):
        self.image, self.attack_imae = None, None

    def read_image(self, image_path, plot=True):
        """read image from file 

        Args:
            image_path (str): iamge file 
            plot (bool, optional): whether ploting image after reading that. Defaults to True.
        """
        self.image = cv2.imread(image_path)[:, :, ::-1]
        if plot:
            plt.imshow(self.image)

    def pred(self, image_path=None, plot=False, return_tensor=False):
        """predicate image. If not read, then read image firstly. 

        Args:
            image_path ([type], optional): if do not read image firstly, you should provide image file. Defaults  None.
            plot (bool, optional): whether ploting image after modifying. Defaults False.

        Raises:
            SystemExit: if do not read image firstly and do not give file path, then raise error. 

        Returns:
            DataFrame:Prediction of image
        """
        # check if the image has been read.
        if not isinstance(self.image, np.ndarray):
            # check if providing image path
            if not image_path:
                raise SystemExit("PLEASE ENTER IMAGE PATH!!")
            self.read_image(image_path)

        self.image = preprocess_input(self.image)
        # check if ploting image after modifying
        if plot:
            plt.imshow(self.image)
        # get prediction
        pred = self.model(self.image.reshape(1, *self.image.shape))

        if return_tensor:
            return pred

        pred_df = pd.DataFrame(decode_predictions(pred.numpy(), top=3)[0],
                               columns=['code', 'label', 'prob'])
        # get label
        label = pred_df.iloc[0, 1]

        return pred_df

    def pred_attack(self):
        """predicte attack image

        Returns:
            DataFrame:Prediction of attac image
        """
        adv_pred = self.model(self.attack_image)

        pred_df = pd.DataFrame(decode_predictions(adv_pred.numpy(), top=3)[0],
                               columns=['code', 'label', 'prob'])

        label = pred_df.iloc[0, 1]

        return pred_df

    def show_diff(self, plot=False):
        """plot diff between image and attack image

        Returns:
           np.array: diff
        """
        diff = (self.attack_image[0, :, :, :] - self.image)
        if plot:
            plt.imshow(diff)
        return diff

    def step(self):
        pass

    def attack(self):
        pass
