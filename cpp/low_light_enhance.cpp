// 导入头文件
#include "lime.h"
#include <vector>
#include <iostream>

/*
LIME算法是一个简单而高效的低光照图像增强算法。
该算法首先通过在R、G和B通道中找到最大值来单独估计每个像素的照明；
然后我们通过在初始光照图上施加一个结构先验来细化它，作为最终的光照映射；最后根据光照映射就可以生成最终的增强图像
参考github链接：https://github.com/zj611/LIME_Processing
*/

/*
该算法优点：能够较好的处理一些低光照片
该算法缺点：LIME算法增强分=之后的图片的色彩不怎么理想
*/
// 定义命名空间
namespace feature
{
    // 获取原图像的通道
    lime::lime(cv::Mat src)
    {
        channel = src.channels();
    }

    cv::Mat lime::lime_enhance(cv::Mat &src)
    {
        cv::Mat img_norm;
        // 图像归一化
        src.convertTo(img_norm, CV_32F, 1 / 255.0, 0);
        // 提前分配空间
        cv::Size sz(img_norm.size());
        cv::Mat out(sz, CV_32F, cv::Scalar::all(0.0));

        auto gammT = out.clone();
        // 根据通道做不同的处理
        if (channel == 3)
        {
            Illumination(img_norm, out);
            Illumination_filter(out, gammT);

            //lime
            std::vector<cv::Mat> img_norm_rgb;
            cv::Mat img_norm_b, img_norm_g, img_norm_r;

            cv::split(img_norm, img_norm_rgb);

            img_norm_g = img_norm_rgb.at(0);
            img_norm_b = img_norm_rgb.at(1);
            img_norm_r = img_norm_rgb.at(2);

            cv::Mat one = cv::Mat::ones(sz, CV_32F);

            float nameta = 0.9;
            auto g = 1 - ((one - img_norm_g) - (nameta * (one - gammT))) / gammT;
            auto b = 1 - ((one - img_norm_b) - (nameta * (one - gammT))) / gammT;
            auto r = 1 - ((one - img_norm_r) - (nameta * (one - gammT))) / gammT;

            cv::Mat g1, b1, r1;

            //TODO <=1
            threshold(g, g1, 0.0, 0.0, 3);
            threshold(b, b1, 0.0, 0.0, 3);
            threshold(r, r1, 0.0, 0.0, 3);

            img_norm_rgb.clear();
            img_norm_rgb.push_back(g1);
            img_norm_rgb.push_back(b1);
            img_norm_rgb.push_back(r1);

            cv::merge(img_norm_rgb,out_lime);
            out_lime.convertTo(out_lime,CV_8U,255);

        }
        else if(channel == 1)
        {
            Illumination_filter(img_norm, gammT);
            cv::Mat one = cv::Mat::ones(sz, CV_32F);
            float nameta = 0.9;
            //std::cout<<img_norm.at<float>(1,1)<<std::endl;
            auto out = 1 - ((one - img_norm) - (nameta * (one - gammT))) / gammT;

            threshold(out, out_lime, 0.0, 0.0, 3);

            out_lime.convertTo(out_lime,CV_8UC1,255);

        }
        else
        {
            std::cout<<"There is a problem with the channels"<<std::endl;
            exit(-1);
        }
        return out_lime.clone();
    }

    void lime::Illumination_filter(cv::Mat& img_in,cv::Mat& img_out)
    {
        int ksize = 5;
        //mean filter
        blur(img_in,img_out,cv::Size(ksize,ksize));
        //GaussianBlur(img_in,img_mean_filter,Size(ksize,ksize),0,0);

        //gamma
        int row = img_out.rows;
        int col = img_out.cols;
        float tem;
        float gamma = 0.8;
        for(int i=0;i<row;i++)
        {
            for(int j=0;j<col;j++)
            {
                tem = pow(img_out.at<float>(i,j),gamma);
                tem = tem <= 0 ? 0.0001 : tem;  //  double epsolon = 0.0001;
                tem = tem > 1 ? 1 : tem;

                img_out.at<float>(i,j) = tem;
            }
        }
    }
    void lime::Illumination(cv::Mat& src,cv::Mat& out)
    {
        int row = src.rows, col = src.cols;
        for(int i=0;i<row;i++)
        {
            for(int j=0;j<col;j++)
            {
                out.at<float>(i,j) = lime::compare(src.at<cv::Vec3f>(i,j)[0],
                                                   src.at<cv::Vec3f>(i,j)[1],
                                                   src.at<cv::Vec3f>(i,j)[2]);
            }
        }
    }
}
