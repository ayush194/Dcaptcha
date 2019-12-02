# Dcaptcha: Optical Character Recognition
          _                 _       _           
       __| | ___ __ _ _ __ | |_ ___| |__   __ _ 
      / _` |/ __/ _` | '_ \| __/ __| '_ \ / _` |
     | (_| | (_| (_| | |_) | || (__| | | | (_| |
      \__,_|\___\__,_| .__/ \__\___|_| |_|\__,_|
                     |_|                        

---------------

Dcaptcha is a simple captcha decoder built for course CS771 (Machine Learning). Our technique is novel and simple. First we run the captcha through some basic image processing including Edge Detection, Dilation and Contour Finding to remove the background color, noise and other latent stuff. Once this is complete, the image is segmented using a Horizontal Histogram with some custom parameters. The individual segments are then fed into the classifier which is pretrained with thousands of data points containing straight/askew pictures of alphabets (The training set can be found in the directory train/). The classifier classifies the sements into one of the 26 classes (corresposnfing to the 26 letters of English Alphabet). The letters are concatenated to return the result (number of characters in captcha, the captcha string itself).

---------------

## Build Instructions

1. To build the project, you need Python3 Interpreter and the following libraries,
    1. OpenCV 3.0 or above
    2. Numpy
    3. Pillow
    4. Cython
    5. Tensorflow 2.0 or above
    6. Keras
You can install the latter 5 using pip3 which comes packaged with Python3.
```
sudo apt-get install libopencv-dev
pip3 install -r requirements.txt
```

2. To train the classifier simply run the script train.py. It trains the classifier using the training dataset for character recognition provided in the data directory.
```
python3 train.py
```

3. To test the classfier, simply run the script eval.py. It runs the Image Processing and subsequently the neural network on the sample images provided in the test directory. It also reads the correct image labels from the codes.txt file and thuss evaluates the accuracy of the classifier.
```
python3 eval.py
```

4. In case running eval.py gives linking errors (linking errors might arise if your opencv version is not the same as the one this library was compiled with i.e. 3.4.4), recompile the shared library Preprocessor.so before runnning eval.py,
```
sh cythonize.sh
```


## Alternate Build using Docker

To perform this build, you need to have [Docker](https://www.docker.com/) installed on your system. If not follow the instructions below to get it running.

### Installing Docker

1. To install docker on Ubuntu 16.04, first add the GPG key for the official Docker repository to the system and add the Docker repository to APT sources,
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

2. Then update the package database with the Docker packages from the newly added repo,
```
sudo apt-get update
```

3. Make sure you are about to install from the Docker repo instead of the default Ubuntu 16.04 repo,
```
apt-cache policy docker-ce
```
You should see the output of the above command as something similar to this,
```
docker-ce:
    Installed: (none)
    Candidate: 17.03.1~ce-0~ubuntu-xenial
    Version table:
        17.03.1~ce-0~ubuntu-xenial 500
            500 https://download.docker.com/linux/ubuntu xenial/stable amd64 Packages
        17.03.0~ce-0~ubuntu-xenial 500
            500 https://download.docker.com/linux/ubuntu xenial/stable amd64 Packages
```

4. Finally install docker,
```
sudo apt-get install -y docker-ce
```

### Creating a docker container

1. Now that docker is installed, create a docker image using the Dockerfile provided. First cd into the repository and then run the command,
```
docker build -t dcaptcha .
```

2. Now create a new docker container using the image we just created,
```
docker create -i -t dcaptcha
```

3. Now start the docker container and navigate to /home/dcaptcha and train/test your data set. (To get the container id run) 
```
container_id=`docker ps -l | tail -n 1 | cut -d " " -f 1`
docker start -i -a $container_id
cd /home/ocr/
python3 train.py
python3 eval.py
```
