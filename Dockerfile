FROM spmallick/opencv-docker:opencv
WORKDIR /root/demo/cpp/OpenCV-3.4.4/

RUN (cd build; cmake ..; cmake --build . --config Release; cd ..;)

WORKDIR /home/
RUN mkdir ocr
ADD . ocr/
RUN pip3 install -r ocr/requirements.txt

RUN (cd ocr; python3 train.py; python3 eval.py;)