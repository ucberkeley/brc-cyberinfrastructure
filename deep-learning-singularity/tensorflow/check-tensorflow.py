# Simple script to check that TensorFlow is working with GPU support

import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
print(tf.__version__)
print('GPU is available: ', tf.test.is_gpu_available())
