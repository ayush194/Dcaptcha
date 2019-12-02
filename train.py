#from __future__ import print_function
#from __future__ import absolute_import, division, print_function, unicode_literals

from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Flatten
from keras.utils import np_utils


from PIL import Image
import numpy as np
#import cv2

import pathlib
data_dir = pathlib.Path("data")
class_names= np.array([item.name for item in data_dir.glob('*') if item.name != "LICENSE.txt"])

dim = 30
#size = (30, 30)
num_pixels = dim * dim
x_train = np.zeros((0, dim, dim, 1))
y_train = np.zeros((0,))

x_test = np.zeros((0, dim, dim, 1))
y_test = np.zeros((0,))

#print(class_names)
for class_name in class_names:
    #print(class_name)
    chars = list(data_dir.glob(class_name+'/*'))
    x = np.array([np.array(Image.open(image_path).resize((dim, dim))).reshape(dim ,dim, 1) for image_path in chars])
    y = np.array([ord(class_name) - ord('A') for image_path in chars])
    #n = int(len(y) * 0.7)
    n = int(len(y))
    x_train = np.concatenate((x_train, x[:n,:,:,:]))
    y_train = np.concatenate((y_train, y[:n]))
    x_test = np.concatenate((x_test, x[:n,:,:,:]))
    y_test = np.concatenate((y_test, y[:n]))
    #print(x_train.shape)
    #print(x_test.shape)


# normalize inputs from 0-255 to 0-1
x_train = x_train / 255
x_test = x_test / 255

print(x_train.shape)
print(y_train.shape)

print(x_test.shape)
print(y_test.shape)

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = len(class_names)

def larger_model():
    # create model
    model = Sequential()
    model.add(Conv2D(3, (5, 5), input_shape=(dim, dim, 1), activation='relu'))
    model.add(MaxPooling2D())
    #model.add(Conv2D(1, (3, 3), activation='relu'))
    #model.add(MaxPooling2D())
    #model.add(Dropout(0.2))
    model.add(Flatten())
    #model.add(Dense(128, activation='relu'))
    #model.add(Dense(10, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# build the model
model = larger_model()
# Fit the model
model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=40, batch_size=200, verbose=2)

#tf.saved_model.save(model, "model")
model.save("model.h5")
# Final evaluation of the model
scores = model.evaluate(x_test, y_test, verbose=0)
print(scores)
print("Baseline Error: %.2f%%" % (100-scores[1]*100))
'''
for i in range(len(x_test)):
    y_predicted = model.predict(x_test[i:i+1])
    #print(x_test[i:i+1].shape)
    max1 = max(y_predicted[0])
    max1_idx = np.argmax(y_predicted[0])
    
    if (max1 < 0.95):
        #rotate and predict again
        idx = max1_idx
        ans = []
        for rot in [-30, 30]:
            img = x_test[i:i+1,:].reshape(size)
            rotated_img = rotateImage(img, rot)
            y_predicted2 = model.predict(rotated_img.reshape(1, num_pixels))
            if (max(y_predicted2[0]) > max1):
                max1_idx = np.argmax(y_predicted2[0])
                y_predicted = y_predicted2
                max1 = max(y_predicted2[0])

    predicted = chr(ord('A') + max1_idx)
    actual = chr(ord('A') + np.argmax(y_test[i]))
    print(predicted)
    print(actual)
    print(y_predicted[0])
    print(y_test[i])
    if (predicted != actual):
        #show image
        cv2.imshow("asdfs", x_test[i:i+1,:].reshape(size) * 255)
        cv2.waitKey(0)
    print(" ")
'''
