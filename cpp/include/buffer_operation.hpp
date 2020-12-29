#include "base.hpp"

cv::Mat transBufferToMat(unsigned char* pBuffer, int width, int height, int channel, int nBPB);
int transMatToBuffer(cv::Mat mSrc, unsigned char** ppBuffer, int& width, int& height, int& nBandNum, int& nBPB);
unsigned char* crop_buffer(unsigned char* data,int x_min,int y_min, int crop_width,int crop_height,int width,int channel);
