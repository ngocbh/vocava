from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys
from scipy.io.wavfile import read
import numpy as np
import os
import tensorflow as tf
import time
# pylint: disable=unused-import
from tensorflow.contrib.framework.python.ops import audio_ops as contrib_audio
# pylint: enable=unused-import

FLAGS = None

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

if tf.test.gpu_device_name():
  print('GPU found')
else:
  print("No GPU found")


def read_wav(path):
  sr, data = read(path)
  data = np.array(data, dtype=np.float64)
  if len(data.shape) == 2:
    data = (data[:,0] + data[:,1])/2
  data = data / (1<<15)
  data = np.reshape(data, (len(data), 1))
  return data, sr

def load_graph(filename):
  """Unpersists graph from file as default graph."""
  with tf.gfile.FastGFile(filename, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')


def load_labels(filename):
  """Read in labels, one label per line."""
  return [line.rstrip() for line in tf.gfile.GFile(filename)]

    


def label_wav(wav, sample_rate, labels, graph):
  """Loads the model and labels, and runs the inference to print predictions."""
  if not labels or not tf.gfile.Exists(labels):
    tf.logging.fatal('Labels file does not exist %s', labels)

  if not graph or not tf.gfile.Exists(graph):
    tf.logging.fatal('Graph file does not exist %s', graph)

  # load graph, which is stored in the default session
  load_graph(graph)
  with tf.Session() as sess: 
    softmax_tensor = sess.graph.get_tensor_by_name(FLAGS.output_name)
    clip_duration_samples = int((FLAGS.clip_duration_ms * sample_rate) / 1000)

    #---------------Fake data-------------------#
    # load data from file for testing
    wav_data, sr = read_wav(wav)
    if(sr != sample_rate):
      tf.logging.fatal("Sample rate doesn't match")
    # end

    # recieve data form client
    offset = 100
    data = wav_data[offset: offset + clip_duration_samples]
    print("Len: ", len(data))

    """Runs the audio data through the graph and prints predictions."""
    feed_dicts = {
      FLAGS.input_data_name: data,
      FLAGS.input_rate_name: 1
      }
    predictions, = sess.run(softmax_tensor, feed_dicts)
    score = predictions[-1]
    # send this value to client
    print("Return value:", score)


def main(_):
  """Entry point for script, converts flags to arguments."""
  label_wav(FLAGS.wav, FLAGS.sample_rate, FLAGS.labels, FLAGS.graph)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--wav', 
      type=str, 
      default='', 
      help='Audio file to be identified.')
  parser.add_argument(
      '--graph', 
      type=str, 
      default='minhphuong.pb', 
      help='Model to use for identification.')
  parser.add_argument(
      '--labels', 
      type=str, 
      default='labels.txt', 
      help='Path to file containing labels.')
  parser.add_argument(
      '--input_data_name',
      type=str,
      default='decoded_sample_data:0',
      help='Name of input data node in model.')
  parser.add_argument(
      '--input_rate_name',
      type=str,
      default='decoded_sample_data:1',
      help='Name of input sample rate node in model.')
  parser.add_argument(
      '--output_name',
      type=str,
      default='labels_softmax:0',
      help='Name of output node in model.')
  parser.add_argument(
      '--clip_duration_ms',
      type=int,
      default=2000,
      help='Length of recognition window.')
  parser.add_argument(
      '--sample_rate',
      type=int,
      default=16000,
      help='Sample rate.')
  

  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)