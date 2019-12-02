import cv2
import numpy as np
from scipy.stats import mode
import progressbar
import time

# this function is needed for the createTrackbar step downstream
def nothing(x):
    pass

# read the experimental image

def run(filename, num_chars, orig_filename):
    img_orig = cv2.imread(filename,1)
    img = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY) 

    
    dilatation_size = 1
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (2*dilatation_size + 1, 2*dilatation_size+1), (dilatation_size, dilatation_size))
    im = cv2.dilate(img, element,borderType=cv2.BORDER_REFLECT)

    mask = np.zeros((np.array(im.shape)+2), np.uint8)

    cv2.floodFill(im, mask, (0,0), (255))
    im_edged = cv2.Canny(im, 30, 200) 
    contours, hierarchy = cv2.findContours(im_edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
    cv2.drawContours(im, contours, -1, (255, 255, 255), 3) 

    (r,c) = im.shape;
    for i in range(r):
        for j in range(c):
            if img_orig[i][j][0] == img_orig[0][0][0] and img_orig[i][j][1] == img_orig[0][0][1] and img_orig[i][j][2] == img_orig[0][0][2] :
                im[i][j] = 255


    # SPLIT
    character = False
    hist = []
    for j in range(c):
        ctr = 0
        filled = False
        for i in range(r):
            if(im[i][j] < 255):
                ctr = ctr + 1
                if ctr > 9:
                    filled = True
            else:
                ctr = 0
        if(filled):
            if not character:
                hist.append(j)
                character = True
        else:
            if character:
                hist.append(j)
                character = False

    size = len(hist)//2;

    #CHECK IF SPLITTTING FAILS

    components = 0
    for j in range(size):
        if (hist[2*j+1]-hist[2*j] > 12):
            components = components + 1
            newmtr = im[:,hist[2*j]:hist[2*j+1]+1]
            processChar(newmtr.copy(), j)
    if components != num_chars:
        print(components, num_chars, filename)
        

    # THIS PART IS ONLY FOR GENERATING TESTCASES
    else:
        components = 0
        for j in range(size):
            if (hist[2*j+1]-hist[2*j] > 12):
                newmtr = im[:,hist[2*j]:hist[2*j+1]+1]
                processed = processChar(newmtr.copy(), j)
                char_freq[orig_filename[components]] = char_freq[orig_filename[components]] + 1
                cv2.imwrite(str(orig_filename[components]) + '/' + str(char_freq[orig_filename[components]]) + '.png', processed)
                components = components + 1


# cv2.destroyAllWindows()


def processChar(img, index):
    color = mode(img[img != 255])[0][0]
    img_filter1 = np.where(img != color, 255, img)
    img_filter2 = np.where(img_filter1 == color, 0, img_filter1)
    square_img = make_square_np(img_filter2)
    # cv2.imshow(str(index), square_img)
    # cv2.waitKey(0)
    return square_img


def make_square_np(img):
    s = max(img.shape[0:2])
    f = np.ones((s,s),np.uint8) * 255
    ax,ay = (s - img.shape[1])//2,(s - img.shape[0])//2
    f[ay:img.shape[0]+ay,ax:ax+img.shape[1]] = img
    return f
    



# run('test/image1.png')

char_freq = {
    'Q':0,
    'W':0,
    'E':0,
    'R':0,
    'T':0,
    'Y':0,
    'U':0,
    'I':0,
    'O':0,
    'P':0,
    'A':0,
    'S':0,
    'D':0,
    'F':0,
    'G':0,
    'H':0,
    'J':0,
    'K':0,
    'L':0,
    'Z':0,
    'X':0,
    'C':0,
    'V':0,
    'B':0,
    'N':0,
    'M':0
}

ctr = 0
arr = input().split()
n = len(arr)

# for name in arr:
#     run('../train/'+ name, len(name) - 4, name)

for i in progressbar.progressbar(range(n)):
    name = arr[i]
    run('../train/'+ name, len(name) - 4, name)