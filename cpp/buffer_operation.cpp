#include "buffer_operation.hpp"

cv::Mat transBufferToMat(unsigned char* pBuffer, int width, int height, int channel, int nBPB){
     cv::Mat mDst;
    if (channel == 3){
        if (nBPB == 1){
            mDst = cv::Mat::zeros(cv::Size(width, height), CV_8UC3);
        }
        else if (nBPB == 2){
            mDst = cv::Mat::zeros(cv::Size(width, height), CV_16UC3);
        }
    }
    else if (channel == 1){
        if (nBPB == 1){
            mDst = cv::Mat::zeros(cv::Size(width, height), CV_8UC1);
        }
        else if (nBPB == 2){
            mDst = cv::Mat::zeros(cv::Size(width, height), CV_16UC1);
        }
    }

    else if(channel == 4){
        if (nBPB == 1){
            mDst = cv::Mat::zeros(cv::Size(width, height), CV_8UC4);
        }
        else if (nBPB == 2){
            mDst = cv::Mat::zeros(cv::Size(width, height), CV_16UC4);
        }
    }

    for (int j = 0; j < height; ++j){
        unsigned char* data = mDst.ptr<unsigned char>(j);
        unsigned char* pSubBuffer = pBuffer + (height - 1 - j) * width  * channel * nBPB;
        memcpy(data, pSubBuffer, width * channel * nBPB);
    }
    if (channel == 3){
        cv::cvtColor(mDst, mDst, CV_RGB2BGR);
    }
    else if (channel == 1){
        cv::cvtColor(mDst, mDst, CV_GRAY2BGR);
    }
    else if (channel == 4){
        cv::cvtColor(mDst, mDst, CV_RGBA2BGR);
    }
    return mDst;
}

int transMatToBuffer(cv::Mat mSrc, unsigned char** ppBuffer, int& width, int& height, int& nBandNum, int& nBPB){
    if (*ppBuffer){
        delete[] * ppBuffer;
        *ppBuffer = nullptr;
    }

    width = mSrc.cols;
    height = mSrc.rows;
    nBandNum = mSrc.channels();
    nBPB = (mSrc.depth() >> 1) + 1;

    size_t nMemSize = width * height * nBandNum * nBPB;
    *ppBuffer = new uchar[nMemSize];
    memset(*ppBuffer, 0, nMemSize);
    uchar* pT = *ppBuffer;
    for (int j = 0; j < height; ++j){
        unsigned char* data = mSrc.ptr<unsigned char>(j);
        unsigned char* pSubBuffer = *ppBuffer + (j)* width  * nBandNum * nBPB;
        memcpy(pSubBuffer, data, width * nBandNum * nBPB);
    }
    return 0;
}

unsigned char* crop_buffer(unsigned char* data,int x_min,int y_min, int crop_width,int crop_height,int width,int channel){
    /*
    在工程代码中实现方式：
    unsigned char* data_crop = (unsigned char*)malloc(crop_width * crop_height * channel * sizeof(unsigned char));
    unsigned char* crop_buffer(unsigned char* data,unsigned char* data_crop,int x_min,int y_min, int crop_width,int crop_height,int width,int channel){
        for(int i=0;i<crop_height;++i){
        memcpy(&data_crop[(i * crop_width) * channel], &data[((i + y_min) * width + x_min) * channel],crop_width * channel);
    }
    *
    此处省略代码，记得一定要把分配的内存释放掉
    * 
    free(data_crop);
    */
    unsigned char* data_crop = (unsigned char*)malloc(crop_width * crop_height * channel);
    for(int i=0;i<crop_height;++i){
        memcpy(&data_crop[(i * crop_width) * channel], &data[((i + y_min) * width + x_min) * channel],crop_width * channel);
    }
    return data_crop;
}