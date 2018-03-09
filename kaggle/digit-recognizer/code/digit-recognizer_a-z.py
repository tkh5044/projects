#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 17:25:55 2018

@author: tkh5044
"""

import pandas as pd
import numpy as np


# Importing Keras libraries and packages
from keras.models import Sequential, Model
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D




train = pd.read_csv('../data/train.csv')
test = pd.read_csv('../data/test.csv')

print (train.shape)
print (test.shape)
train.head()

Y_train_orig = np.array([train.label])
X_train_orig = np.array([train.iloc[i, 1:] for i in range(len(train))])
X_test_orig = np.array([test.iloc[i, :] for i in range(len(test))])

X_train_split = np.array([np.split(i, 28) for i in X_train_orig])
X_test_split = np.array([np.split(i, 28) for i in X_test_orig])

Y_train = Y_train_orig.T
X_train = X_train_split/255.
X_test = X_test_split/255.

X_train = np.expand_dims(X_train, axis=-1)
X_test = np.expand_dims(X_test, axis=-1)


print ("number of training examples = " + str(X_train.shape[0]))
print ("number of test examples = " + str(X_test.shape[0]))
print ("Y_train shape: " + str(Y_train.shape))
print ("X_train shape: " + str(X_train.shape))
print ("X_test shape: " + str(X_test.shape))


# Initializing the CNN
classifier = Sequential()

# Step 1 - Convolution
classifier.add(Conv2D(32, (3, 3), padding='same', input_shape=(64, 64, 3), activation='relu'))

# Step 2 - Max Pooling
classifier.add(MaxPooling2D((2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Dense
classifier.add(Dense(128, activation='relu'))
classifier.add(Dense(1, activation='sigmoid'))

# Compiling the CNN
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])



def cnn_model(input_shape):
    """    
    Arguments:
    input_shape -- shape of the images of the dataset

    Returns:
    model -- a Model() instance in Keras
    """
    
    # define the input placeholder as a tensor with shape input_shape (kinda like the input image)
    X_input = Input(input_shape)

    # pad the border of X_input with zeroes
    X = ZeroPadding2D((3, 3))(X_input)

    # CONV -> BN -> RELU Block applied to X
    X = Conv2D(32, (3, 3), strides = (1, 1), name = 'conv0')(X)
    X = BatchNormalization(axis = 3, name = 'bn0')(X)
    X = Activation('relu')(X)

    # MAXPOOL
    X = MaxPooling2D((2, 2), name='max_pool')(X)

    # convert X to a vector + FULLYCONNECTED
    X = Flatten()(X)
    X = Dense(128, activation='relu')(X)
    X = Dense(1, activation='sigmoid', name='fc')(X)

    # create Keras model instance to be used to train/test the model
    model = Model(inputs = X_input, outputs = X, name='HappyModel')
        
    return model


digit_recog = cnn_model(X_train[0].shape)

digit_recog.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

digit_recog.fit(x=X_train, y=Y_train, epochs=15, batch_size=32)
