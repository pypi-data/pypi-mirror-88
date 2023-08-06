
import sys
import os
import tensorflow as tf
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sann.bin import config
from sann.bin import data_utils





class Model(tf.keras.Model):
    def __init__(self,trainable,initial_weigh):
        super().__init__()
        self.large = tf.keras.layers.Dense(300)
        self.large2 = tf.keras.layers.Dense(800)
        self.dropout = tf.keras.layers.Dropout(config.config.drop_rate)
        self.out_layer = tf.keras.layers.Dense(data_utils.utils.cla_num,activation='softmax')

    def call(self, x):
        x = self.large(x)
        x = self.large2(x)
        x = self.dropout(x)
        x = self.out_layer(x)
        return x