#include "optical_processing.hpp"

//去除光照不均匀
void uneven_light_compensate(Mat &image, int blockSize=32)
{
	/*
	1、求取源图I的平均灰度，并记录rows和cols；
	2、按照一定大小，分为N*M个方块，求出每块的平均值，得到子块的亮度矩阵D；
	3、用矩阵D的每个元素减去源图的平均灰度，得到子块的亮度差值矩阵E；
	4、用双立方差值法，将矩阵E差值成与源图一样大小的亮度分布矩阵R；
	5、得到矫正后的图像result=I-R；
	*/
	if (image.channels() == 3) cv::cvtColor(image, image, 7);
	double average = mean(image)[0];
	int rows_new = ceil(double(image.rows) / double(blockSize));
	int cols_new = ceil(double(image.cols) / double(blockSize));
	cv::Mat blockImage;
	blockImage = cv::Mat::zeros(rows_new, cols_new, CV_32FC1);
	for (int i = 0; i < rows_new; i++)
	{
		for (int j = 0; j < cols_new; j++)
		{
			int rowmin = i*blockSize;
			int rowmax = (i + 1)*blockSize;
			if (rowmax > image.rows) rowmax = image.rows;
			int colmin = j*blockSize;
			int colmax = (j + 1)*blockSize;
			if (colmax > image.cols) colmax = image.cols;
			cv::Mat imageROI = image(Range(rowmin, rowmax), Range(colmin, colmax));
			double temaver = mean(imageROI)[0];
			blockImage.at<float>(i, j) = temaver;
		}
	}
	blockImage = blockImage - average;
	cv::Mat blockImage2;
	resize(blockImage, blockImage2, image.size(), (0, 0), (0, 0), INTER_CUBIC);
	cv::Mat image2;
	image.convertTo(image2, CV_32FC1);
	cv::Mat dst = image2 - blockImage2;
	dst.convertTo(image, CV_8UC1);
}