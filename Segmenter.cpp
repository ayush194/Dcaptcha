#include "Segmenter.h"
#define IMAGE_SIZE 30

Segmenter::Segmenter() {}

std::vector<std::vector<float>> Segmenter::segment(std::vector<std::string> filenames) {
    std::vector<std::vector<float>> return_to_python;
    int components = 0;
    for(std::string filename : filenames) {
        cv::Mat original_image = cv::imread(filename, 1);
        cv::Mat image;
        cv::cvtColor(original_image, image, CV_BGR2GRAY);
        int rows = image.rows;
        int cols = image.cols;

        if (image.empty()) {
            std::cout << "Empty Image" << std::endl;
        }

        int dilation_size = 1;
        cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT,
                        cv::Size( 2*dilation_size + 1, 2*dilation_size+1 ),
                        cv::Point( dilation_size, dilation_size ));
        cv::Mat dilated_image(rows, cols, CV_8U);
        cv::dilate(image, dilated_image, element, cv::Point(-1,-1), 1, cv::BORDER_REFLECT);

        cv::Mat floodfill_mask = cv::Mat::zeros(rows + 2, cols + 2, CV_8U);
        
        cv::floodFill(dilated_image, floodfill_mask, cv::Point(0, 0), 255);
        cv::Mat dilated_canny_image(rows, cols, CV_8U);
        cv::Canny(dilated_image, dilated_canny_image, 30, 200);

        std::vector<std::vector<cv::Point>> contours;
        std::vector<cv::Vec4i> hierarchy;
        cv::findContours(dilated_canny_image, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);
        cv::drawContours(dilated_image, contours, -1, cv::Scalar(255, 255, 255), 3);

        //remove background
        cv::Vec3b top_left = original_image.at<cv::Vec3b>(0, 0);
        for(int i = 0; i < rows; i++) {
            uchar* row = dilated_image.ptr<uchar>(i);
            cv::Vec3b* original_row = original_image.ptr<cv::Vec3b>(i);
            for(int j = 0; j < cols; j++) {
                if (top_left[0] == original_row[j][0] && top_left[1] == original_row[j][1] && top_left[2] == original_row[j][2]) {
                    row[j] = 255u;
                }
            }
        }

        bool character = false;
        std::vector<float> hist;
        for(int j = 0; j < cols; j++) {
            int ctr = 0;
            bool filled = false;
            for(int i = 0; i < rows; i++) {
                if (dilated_image.at<uchar>(i, j) < 255u) {
                    ctr++;
                    if (ctr > 9) filled = true;
                } else {
                    ctr = 0;
                }
            }
            if (filled) {
                if (!character) {
                    hist.push_back(j);
                    character = true;
                }
            } else {
                if (character) {
                    hist.push_back(j);
                    character = false;
                }
            }
        }

        int size = hist.size() / 2;
        int n_chars = 0;
        for(int t = 0; t < size; t++) {
            if (hist[2*t+1]-hist[2*t] > 12) {
                int n_cols = hist[2*t+1]-hist[2*t]+1;
                cv::Mat new_image(std::max(rows, n_cols), std::max(rows, n_cols), CV_8U, cvScalar(255));
                int x_offset = (new_image.cols - n_cols) / 2;
                int y_offset = (new_image.rows - rows) / 2;
                std::vector<int> freq(256,0);

                uchar mode_color = 0;
                for(int i=0; i<rows; i++){
                    for(int j=0, j_orig=hist[2*t]; j_orig<=hist[2*t+1]; j_orig++,j++){
                        uchar color = dilated_image.at<uchar>(i, j_orig);
                        new_image.at<uchar>(i + y_offset, j + x_offset) = color;
                        freq[color]++;
                        if(color != 255u && freq[mode_color] < freq[color]){
                            mode_color = color;
                        }
                    }
                }

                for(int i=0; i<new_image.rows; i++){
                    for(int j=0; j<new_image.cols; j++){
                        if(new_image.at<uchar>(i,j) == mode_color){
                            new_image.at<uchar>(i,j) = 0u;
                        } else {
                            new_image.at<uchar>(i,j) = 255u;
                        }
                    }
                }
                
                cv::Mat resized_image;
                cv::resize(new_image, resized_image, cv::Size(IMAGE_SIZE, IMAGE_SIZE), 0, 0, CV_INTER_LINEAR);

                return_to_python.push_back({});
                for(int i=0; i<resized_image.rows; i++){
                    for(int j=0; j<resized_image.cols; j++){
                        return_to_python[components].push_back(float(resized_image.at<uchar>(i,j) / 255));
                    }
                }
                components++;
                n_chars++;
            }
        }
        this->num_chars.push_back(n_chars);
    }
    return return_to_python;
    //cv::imshow("image", dilated_image);
    //cv::waitKey(0);
}

/*
int main() {
    Segmenter mysegmenter;
    //mysegmenter.segment("train/AAA.png");

    int n;
    std::cin >> n;
    std::string s;
    for(int i=0;i<n;i++){
        std::cin >> s;
        mysegmenter.segment("train/" + s);
    }
    
    return 0;
}
*/
//link dynamic libraries
//-lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lopencv_highgui