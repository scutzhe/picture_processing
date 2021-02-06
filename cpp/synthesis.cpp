#include "base.hpp"

cv::Mat synthesis_simple_image(cv::Mat Image,cv::Mat mask,int* coordination)
{
    /*
    cv::Mat Image 原图
    cv::Mat mask  待贴图片
    int* coordination 贴图片左上角的位置
    利用ROI将一幅图像叠加到另一幅图像的指定位置
    */
	// 【1】获取原始图片和待贴图片
	if (!Image.data || !mask.data)
	{
		cout << "读取图像有误，请重新输入正确路径！\n";
		return false;
	}
	//【2】定义一个Mat类型并给其设定ROI区域
	cv::Mat imageROI = Image(Rect(coordination[0], coordination[1], mask.cols, mask.rows));
	//【3】加载掩模（必须是灰度图）
	//Mat mask = cv::imread("tim.jpg", 0);	//参数0显示为灰度图
	//【4】将掩模复制到ROI
	mask.copyTo(imageROI, mask);   //这句很重要，一定要用mask下的操作
	//【5】显示结果
//	cv::namedWindow("利用ROI实现图像叠加");
//	cv::imshow("利用ROI实现图像叠加", Image);
    return imshowRoI;
}