import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.preprocessing import image
from tensorflow.keras import backend as K
from tensorflow.keras import models
from tensorflow.keras.applications.vgg16 import (VGG16, decode_predictions,
                                                 preprocess_input)


class CamHeatMap:
    """HeatMap Visualization for CAM"""
    def __init__(self, model):
        """init parameters

        Args:
            model : tensorflow model .
        """
        self.model = model

    def read_image(self,
                   img_path,
                   target_size=(224, 224),
                   preprocess_input=preprocess_input):
        """read image from file 

        Args:
            img_path (str): image file
            target_size (tuple, optional): target size of image. Defaults to (224, 224).

        Returns:
            tensor: iamge after propressing
        """
        # read image
        img = image.load_img(img_path, target_size=target_size)
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)

        return preprocess_input(img)

    def cam(self,
            img_path,
            layer='block5_conv3',
            output='output_heatmap.jpeg',
            decode_predictions=decode_predictions):
        """ Plot heat map for layer 

        Args:
            img_path (str): iamge file
            layer (str, optional): layer slected to plot. Defaults to 'block5_conv3'.
            output (str, optional): whether outouting heatmap . Defaults to 'output_heatmap.jpeg'.
        """
        # read image
        image_array = self.read_image(img_path)
        # get layers from model
        current_layer = self.model.get_layer(layer)
        build_heatmap = models.Model([self.model.inputs],
                                     [current_layer.output, self.model.output])
        # gradient descent
        with tf.GradientTape() as tape:
            layer_results, predictions = build_heatmap(image_array)
            loss = predictions[:, np.argmax(predictions[0])]

        # get prediction and related labels
        prediction = self.model.predict(image_array)
        label = pd.DataFrame(decode_predictions(prediction, top=3)[0],
                             columns=['code', 'label',
                                      'probability']).iloc[0, 1]
        # compute gradient
        gradients = tape.gradient(loss, layer_results)
        pooled = K.mean(gradients, axis=(0, 1, 2))
        # build out the heatmap
        raw_heatmap = tf.reduce_mean(tf.multiply(pooled, layer_results),
                                     axis=-1)
        raw_heatmap = np.maximum(raw_heatmap, 0)
        # don't want a value of 0
        maximum_heatmap = np.max(raw_heatmap)
        if maximum_heatmap == 0:
            maximum_heatmap = 1e-10
        # normalize based on max value
        raw_heatmap /= maximum_heatmap
        # visualize
        visual_map = raw_heatmap[0, :, :]
        visual_map = np.ones(visual_map.shape) - visual_map  # invert it
        # read raw image
        img = cv2.imread(img_path)

        adjustment = 255
        raw_heatmap = cv2.resize(visual_map, (img.shape[1], img.shape[0]))
        raw_heatmap = np.uint8(adjustment * raw_heatmap)
        raw_heatmap = cv2.applyColorMap(raw_heatmap, cv2.COLORMAP_JET)

        # ouput heatmap
        overlay = raw_heatmap * 0.8 + img
        cv2.imwrite(output, overlay)

        # plot heatmap
        img = mpimg.imread(output)
        plt.imshow(img[:, :, ::-1])
        plt.axis('off')
        return (img[:, :, ::-1], label)

    def show_all_layers_block(self, image_path, output=False):
        """show heatmap for all layers  

        Args:
            image_path (str): image file
        """
        all_layers = []

        for layer in self.model.layers:
            # check for convolutional layer
            if isinstance(layer, tf.python.keras.layers.convolutional.Conv2D):
                all_layers.append(layer.name)
        # plot
        fig, axs = plt.subplots(4, 3)

        ind = 0

        for i in range(4):
            for j in range(3):
                ax = axs[i, j]
                ax.set_xticks([])
                ax.set_yticks([])
                cam_img, label = self.cam(image_path, all_layers[ind])
                ax.imshow(cam_img)
                ind += 1

        fig.set_size_inches(12, 12)
        plt.show()
        fig.set_size_inches(12, 12)
        plt.title(label)
        plt.imshow(self.cam(image_path, all_layers[-1])[0])
        plt.show()
