import cv2
import feature_extraction as f_ext
from sklearn import svm
from sklearn.externals import joblib
import numpy as np
import glob

# contents = glob.glob(r'D:\CDSAML_2019\Gait_IR\CT\NEW\*.mp4')
contents = glob.glob(r'E:\Softwares\PyCharm\PyCharm Community Edition 2018.2.4\Projects\Gait Analysis\Valid_videos\*.mp4')
train_vector = []
responses = []

for path in contents:
    video = cv2.VideoCapture(path)
    gait_cycle_estimate = f_ext.calc_gait_cycle(video)

    # gait_cycle_estimate[0]     : Number of steps in given gait sequence
    # gait_cycle_estimate[1]     : Size of rectangles in each gait step
    # gait_cycle_estimate[2]     : Number of frames in each step
    # gait_cycle_estimate[3]     : Distance between feet in each frame
    # gait_cycle_estimate[4]     : Haar wavelet coefficients found using 2D-DWT

    spatial_feature_vector = f_ext.calc_spatial_component(gait_cycle_estimate[0], gait_cycle_estimate[1],
                                                          gait_cycle_estimate[2])
    # spatial_feature_vector[0]    : mean height of bounding rectangle
    # spatial_feature_vector[1]    : mean width of bounding rectangle
    # spatial_feature_vector[2]    : mean angle of bounding rectangle
    # spatial_feature_vector[3]    : mean aspect ratio of bounding rectangle

    temporal_feature_vector = f_ext.calc_temporal_component(gait_cycle_estimate[3])

    # temporal_feature_vector[0]   : length of each step
    # temporal_feature_vector[1]   : length of each stride (2 * step length)
    # temporal_feature_vector[2]   : cadence of subject (number of steps per second)
    # temporal_feature_vector[3]   : velocity of subject ( cadence * 0.5 * stride length)

    wavelet_component = f_ext.calc_wavelet_component(gait_cycle_estimate[4], gait_cycle_estimate[2])

    # mean and standard deviation for 3 coefficients
    # [(mean_1, mean_2, mean_3), (stand_1, stand_2, stand_3)]
    # Wavelet features calculated using 2D Haar DWT

    training_sample = np.concatenate([spatial_feature_vector, temporal_feature_vector, wavelet_component], axis=None)

    label = int(path[(len(path) - 11): (len(path) - 8)])
    responses.append(label)
    train_vector.append(training_sample)

train_vector = np.array(train_vector)
responses = np.array(responses)

max_length = np.max([len(element) for element in train_vector])
train_vector = np.asarray([np.pad(ele, (0, max_length - len(ele)), 'constant', constant_values=0)
                           for ele in train_vector])

# Creating SVM model
clf = svm.SVC(kernel='linear')
clf.fit(train_vector, responses)
joblib.dump(clf, 'SVM_Model.pkl')
print("Training Successful")





