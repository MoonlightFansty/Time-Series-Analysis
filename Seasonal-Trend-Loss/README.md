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

