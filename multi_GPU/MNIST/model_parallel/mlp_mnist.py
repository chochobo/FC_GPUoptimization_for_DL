from __future__ import print_function

import input_data
import time
import numpy as np
mnist = input_data.read_data_sets("/home/deepl/FC/multi-GPU/MNIST/data_mnist", one_hot=True)

import tensorflow as tf

x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])
 

with tf.variable_scope("layer0"):
  W = tf.Variable(tf.truncated_normal([784, 8192], stddev=0.1), name="W")
  b = tf.Variable(tf.truncated_normal([8192], stddev=0.1), name="b")

  local0 = tf.nn.relu(tf.matmul(x, W) + b)

#y0 = local0

with tf.variable_scope("layer1"):
  W = tf.Variable(tf.truncated_normal([8192, 10], stddev=0.1), name="W")
  b = tf.Variable(tf.truncated_normal([10], stddev=0.1), name="b")

  local1 = tf.nn.softmax(tf.matmul(local0, W)+b)
#y1 = local1


cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(local1), reduction_indices=[1]))

opt = tf.train.AdamOptimizer(1e-4)
grads = opt.compute_gradients(cross_entropy)
train_step = opt.apply_gradients(grads)

with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  

  max_steps = 1000
  latency = []

  for step in range(max_steps):
    batch_xs, batch_ys = mnist.train.next_batch(10)
    st = time.time()
    _, loss = sess.run([train_step, cross_entropy], feed_dict={x: batch_xs, y_: batch_ys})
    latency.append(time.time()-st)

    if (step % 10) == 0:
      print("step = ",step, "\tloss = ",loss , "\tstep/sec = ", np.average(latency))
      latency = []
