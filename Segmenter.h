#ifndef SEGMENTER_H
#define SEGMENTER_H

#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <cmath>

#include <vector>
#include <string>

class Segmenter {
    public:
    std::vector<int> num_chars;
    Segmenter();
    std::vector<std::vector<float>> segment(std::vector<std::string>);
};

#endif