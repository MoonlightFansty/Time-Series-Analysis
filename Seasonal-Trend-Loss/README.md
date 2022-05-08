# Seasonal Trend Loss
##  一、STL概念及适用情形
STL的全称是```Seasonal Trend Loss```，是一种滤波方式，可以把时间序列分解为```Trend```、```Seasonal```和```Remainder``` \
STL包含一系列局部加权回归平滑器，计算速度比较快，可以应对非常大的的时间序列数据 

根据原始STL论文为例，下图中的data原始数据可以分解为Trend, Seasonal和Remainder
* Trend表示数据的长期趋势，由图可知Trend是长期增长的 
* Seansonal表示季节性变动，呈现周期性
* Remainder表示原始数据分解完Trend和Seasonal之后的残差 \
![Seasonal Trend Loss]()

## 二、STL的时序分解
以北京PM2.5为例，进行STL方法的时序分解 \
**(1)读取数据** \


