# CS771 ASSIGNMENT-3 BY GROUP-21
# TEAM MEMBERS: Umang Malik (170765), Abhyuday Pandey (170039), Ayush Kumar (170195), Srinjay Kumar (170722), Deepesh Lall (170236)
import numpy as np
from tensorflow import keras
import Preprocessor

dim = 30

mypreprocessor = Preprocessor.Preprocessor()
model = keras.models.load_model('model.h5')

def decaptcha(filenames):
    for i in range(len(filenames)):
        filenames[i] = filenames[i].encode()
    images = np.array(mypreprocessor.segment(filenames))
    num_chars_orig = np.array(mypreprocessor.num_chars)
    num_chars = []
    images = images.reshape(images.shape[0], dim, dim, 1)
    y_predicted = model.predict(images)
    max1 = np.amax(y_predicted, axis=1)
    # max1 will be used for deciding whether we should keep that alphabet or discard
    # (discard when the image which was used for predicting that letter was a combi of lines)
    max1_idx = np.argmax(y_predicted, axis=1)
    letters = ''.join([str(chr(ord('A') + idx)) for idx in max1_idx])
    codes, ctr = [], 0
    for num in num_chars_orig:
        cur_code = letters[ctr:ctr+num]
        if len(cur_code) > 4:
            cur_code = cur_code.replace('I', '', num - 4)
        codes.append(cur_code)
        num_chars.append(len(cur_code))
        ctr = ctr + num
    return num_chars, codes
