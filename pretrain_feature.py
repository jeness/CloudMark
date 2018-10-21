import glob
import numpy as np
from skimage.transform import AffineTransform
import tensorflow as tf
import tensorflow_hub as hub
import pickle

data_list = glob.glob('test/*.jpg')

def image_input_fn(data_list = data_list):
  filename_queue = tf.train.string_input_producer(
      data_list, shuffle=False)
  reader = tf.WholeFileReader()
  _, value = reader.read(filename_queue)
  image_tf = tf.image.decode_jpeg(value, channels=3)
  return tf.image.convert_image_dtype(image_tf, tf.float32)

tf.reset_default_graph()
tf.logging.set_verbosity(tf.logging.FATAL)

m = hub.Module('https://tfhub.dev/google/delf/1')

# The module operates on a single image at a time, so define a placeholder to
# feed an arbitrary image in.
image_placeholder = tf.placeholder(
    tf.float32, shape=(None, None, 3), name='input_image')

module_inputs = {
    'image': image_placeholder,
    'score_threshold': 100.0,
    'image_scales': [0.25, 0.3536, 0.5, 0.7071, 1.0, 1.4142, 2.0],
    'max_feature_num': 1000,
}

module_outputs = m(module_inputs, as_dict=True)

image_tf = image_input_fn(data_list=data_list)
# image_input = image_input_fn(data_list=image_input_path)

with tf.train.MonitoredSession() as sess:
  feature_dict = {}  # Stores the locations and their descriptors for each image stored for test
  for image_path in data_list:
    image = sess.run(image_tf)
    print('Extracting locations and descriptors from %s' % image_path)
    feature_dict[image_path] = sess.run(
        [module_outputs['locations'], module_outputs['descriptors']],
        feed_dict={image_placeholder: image})
# print(feature_dict)
file = open('feature.txt','wb')
pickle.dump(feature_dict,file)

# a = pd.DataFrame(feature_dict)
# np.save('feature.npy', feature_dict)
