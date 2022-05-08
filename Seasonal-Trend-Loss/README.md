# Seasonal Trend Loss
##  一、STL概念及适用情形
STL的全称是```Seasonal Trend Loss```，是一种滤波方式，可以把时间序列分解为```Trend```、```Seasonal```和```Remainder``` \
STL包含一系列局部加权回归平滑器，计算速度比较快，可以应对非常大的的时间序列数据 

根据原始STL论文为例，下图中的data原始数据可以分解为Trend、 Seasonal和Remainder
* Trend表示数据的长期趋势，由图可知Trend是长期增长的 
* Seansonal表示季节性变动，呈现周期性
* Remainder表示原始数据分解完Trend和Seasonal之后的残差 \
![Seasonal Trend Loss]()

## 二、STL的时序分解
以北京PM2.5为例，进行STL方法的时序分解 \
**(1)读取数据** \
```
import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
```
```
# load time series data
air_pollution = pd.read_csv('./dataset/air_pollution.csv', parse_dates=['date']) # parse_dates select index
air_pollution.set_index('date', inplace=True)

values = air_pollution.values
groups = [0, 1, 2, 3, 4, 5, 6, 7]
i = 1
# plot each column
for group in groups:
    plt.subplot(len(groups), 1, i)
    plt.plot(values[:, group])
    plt.title(air_pollution.columns[group], y=0.5, loc='right')
    i += 1

# plt.savefig('air_pollution.png')
plt.show()
```
![air_pollution]()
根据上图可以看到，根据时间有很多相关的因变量 \
在这里，我们采用pollution_today作为因变量，看时间和pollution_today之间的关系
**(2)数据平滑与参数设置**
在做STL分解之前，我们先对时序数据进行平滑，这里采用python中的rolling作为窗口平滑函数，窗口大小选择5，我们拿365个数据，去预测未来10天得数据 
```
window_size = 5   # 这里window_size是做滑动窗口时候的大小，可以按照自己的数据，进行更换
max_points = 365 # 指的是准备做时序分解时候的大小，可以按照自己的数据进行更换
filling_points=10   # 预测多少的未来数据，可以按照自己的数据进行更换
s = air_pollution['pollution_today'][:max_points+filling_points].rolling(window=window_size).mean()
```
**(3)数据补全**
拿到数据后，要再次做滤波和平滑，让原始数据噪音更小。并且也要补充未来10个点的值，在这里，采用均值方法对未来10个点进行补全
```
# 这段方法是用来求平均
def filling_future_points(list, num=10):
    nozero_list = [one for one in list if one != 0]
    before_avg, last_avg = sum(nozero_list[:num]) / num, sum(nozero_list[-1 * num:]) / num
    res_list = []
    for i in range(len(list)):
        if list[i] != 0:
            res_list.append(list[i])
        else:
            tmp = int(num / 2) + 1
            if i <= tmp:
                res_list.append(int(before_avg))
            elif i >= len(list) - tmp:
                res_list.append(int(last_avg))
                slice_list = list[i - tmp:i + tmp + 1]
                res_list.append(int(sum(slice_list) / (num - 1)))
```
补全之后，由于窗口滑动平均，会导致初始的window_size-1个点得数值为空，以及未来的最后window_size-1个点得数据也为空，所以还需要补全一前一后的窗口值
```
filling_list = filling_future_points(air_pollution['pollution_today'][max_points-filling_points:max_points], num=filling_points)
true_result = air_pollution['pollution_today'][max_points:max_points+filling_points]

for i in range(window_size):
    s[i] = air_pollution['pollution_today'][i]
for i in range(max_points, max_points + filling_points):
    s[i] = filling_list[i - max_points]
```
**(4)时序分解**
```
result1 = seasonal_decompose(s, model='multiplicative')
```
可以得到下图:
* 第一个子图是原始数据
* 第二个子图是趋势，可以看到空气污染本身没有趋势
* 第三个图可以看到周期性特别强
* 最后Resid代表了残差
![]()

## 三、模型评估
时间序列的评估一般是采用MSE(Mean Square Error)进行评估的，一般MSE越小，代表和原始的时间序列之间重合度越高
```
def calculate_mse(a, b, lower, upper):
    error = 0
    for i in range(lower, upper):
        error += (a[i] - b[i]) * (a[i] - b[i])
    return error / (upper - lower)


prdict_value = result1.seasonal[-filling_points:] + result1.trend[-filling_points:]
for i in range(max_points, max_points+filling_points):
    if pd.isna(prdict_value[i - max_points]):
        prdict_value[i - max_points] = s[i]
    else:
        continue

mse_error = calculate_mse(prdict_value, true_result, 0, len(true_result))
print(mse_error)
```
