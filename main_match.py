import matplotlib.pyplot as plt
import glob
import matplotlib.image as mpimg
import numpy as np
from scipy.spatial import cKDTree
from skimage.feature import plot_matches
from skimage.measure import ransac
from skimage.transform import AffineTransform
import tensorflow as tf
import tensorflow_hub as hub
import pickle

file = open('feature.txt','rb')
results_dict = pickle.load(file)
data_list = list(results_dict.keys())
image_input_path = glob.glob('input/*.jpg')

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

image_input = image_input_fn(data_list=image_input_path)

with tf.train.MonitoredSession() as sess:
  input_dict = {}   # Stores th locations and their dexcriptors for each input image
  for image_test_path in image_input_path:
    input = sess.run(image_input)
    print('Extracting locations and descriptors from %s' % image_test_path)
    input_dict[image_test_path] = sess.run(
        [module_outputs['locations'], module_outputs['descriptors']],
        feed_dict={image_placeholder: input})

#@title TensorFlow is not needed for this post-processing and visualization
def match_images(results_dict, input_dict, image_1_path, image_2_path):
  distance_threshold = 0.8
  print(image_2_path)
  # Read features.
  locations_1, descriptors_1 = input_dict[image_1_path]
  num_features_1 = locations_1.shape[0]
  # print("Loaded image 1's %d features" % num_features_1)
  locations_2, descriptors_2 = results_dict[image_2_path]
  num_features_2 = locations_2.shape[0]
  # print("Loaded",image_2_path,"'s %dfeatures" % (num_features_2))

  # Find nearest-neighbor matches using a KD tree.
  d1_tree = cKDTree(descriptors_1)
  _, indices = d1_tree.query(
      descriptors_2, distance_upper_bound=distance_threshold)

  # Select feature locations for putative matches.
  locations_2_to_use = np.array([
      locations_2[i,]
      for i in range(num_features_2)
      if indices[i] != num_features_1
  ])
  locations_1_to_use = np.array([
      locations_1[indices[i],]
      for i in range(num_features_2)
      if indices[i] != num_features_1
  ])

  # print(locations_1_to_use)

  # Perform geometric verification using RANSAC.
  # Try to add a try function to solve errors
  if locations_1_to_use.shape[0]!=0:
      _, inliers = ransac(
          (locations_1_to_use, locations_2_to_use),
          AffineTransform,
          min_samples=3,
          residual_threshold=20,
          max_trials=1000)
      if inliers is None:
          return 0, locations_1_to_use, locations_2_to_use, inliers
      else:
          return sum(inliers), locations_1_to_use, locations_2_to_use, inliers
  else:
      return 0, locations_1_to_use, locations_2_to_use, None
  # print('Found %d inliers' % sum(inliers))
  # return sum(inliers)

for test_path in image_input_path:
    matches = []
    test_feature = []
    data_feature = []
    inliers = []
    for data_path in data_list:
        match_num, locations_1_to_use, locations_2_to_use, inlier = match_images(results_dict, input_dict, test_path, data_path)
        # print('has',match,'matches with',data_path)
        matches.append(match_num)
        test_feature.append(locations_1_to_use)
        data_feature.append(locations_2_to_use)
        inliers.append(inlier)
    index = matches.index(max(matches))
    print(test_path)
    print(matches[index],data_list[index])
    # print(inliers[index])


    _, ax = plt.subplots()
    img_1 = mpimg.imread(test_path)
    img_2 = mpimg.imread(data_list[index])
    inlier_idxs = np.nonzero(inliers[index])[0]
    plot_matches(
      ax,
      img_1,
      img_2,
      test_feature[index],
      data_feature[index],
      np.column_stack((inlier_idxs, inlier_idxs)),
      matches_color='b')
    ax.axis('off')
    ax.set_title('DELF correspondences')
    plt.show()
