# coding=utf-8

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "5"

import tensorflow as tf
tf.enable_eager_execution()

import tf_geometric as tfg

import numpy as np

x = tf.Variable(tf.random.truncated_normal([5, 150]))

edge_index = [
    [0, 1, 3, 4],
    [0, 2, 1, 3]
]

graph = tfg.Graph(x, edge_index=[])

fc = tf.keras.layers.Dense(10)

gcn = tfg.layers.GIN(fc)

h = gcn([graph.x, graph.edge_index])



# h = tf.segment_sum(graph.x, [])
print(h)