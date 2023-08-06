import importlib
import tensorflow as tf
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sann.bin import config
from sann.bin import data_utils



class my_layer(tf.keras.layers.Layer):
    def __init__(self,out_num,trainable,initial_weigh):
        super().__init__()
        self.initial_weigh = initial_weigh
        self.trainable = trainable
        self.out_num = out_num
        self.drop_layer = tf.keras.layers.Dropout(config.config.drop_rate)
        self.combination_layer = tf.keras.layers.Dense(out_num)

    def build(self, input_shape):

        if type(self.initial_weigh) != type(None):
            self.kernel_corr = tf.Variable(name='kernel', initial_value=self.initial_weigh[0],
                                      trainable=self.trainable, dtype='float32')
        else:
            self.kernel_corr = self.add_weight(name='kernel',
                                          shape=[input_shape[1], input_shape[1]], trainable=True, dtype='float32')

        if type(self.initial_weigh) != type(None):
            self.kernel_weights = tf.Variable(name='kernel', initial_value=self.initial_weigh[1],
                                      trainable=self.trainable, dtype='float32')
        else:
            self.kernel_weights = self.add_weight(name='kernel',
                                          shape=[input_shape[1], self.out_num], trainable=True, dtype='float32')






    def call(self,input):

        kernel_weights_corr = tf.matmul(self.kernel_corr, self.kernel_weights)


        input = tf.cast(input,tf.float32)


        input = self.drop_layer(input)
        output = tf.matmul(input,kernel_weights_corr)



        return output


class Model(tf.keras.Model):
    def __init__(self,trainable,initial_weigh):
        super().__init__()
        self.layer = my_layer(data_utils.utils.cla_num, trainable=trainable, initial_weigh=initial_weigh)

    def call(self, x):
        x = self.layer(x)
        x = tf.nn.softmax(x,axis=1)
        return x























