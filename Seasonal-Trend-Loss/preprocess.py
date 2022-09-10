import pandas as pd
from matplotlib import pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

# check time series data
data_frame = pd.read_csv('./dataset/air_pollution.csv', parse_dates=['date'])
# parse_dates 设置数据转成时间格式
# read_csv() 指定parse_dates会使得读取csv文件的时间大大增加
data_frame.set_index('date', inplace=True) # 选定index

values = data_frame.values
groups = [i for i in range(len(values[1]))]
print(groups)
i = 1
# plot each column
for group in groups:
    plt.subplot(len(groups), 1, i)
    plt.plot(values[:, group])
    plt.title(data_frame.columns[group], y=0.5, loc='right')
    i += 1

# plt.savefig('air_pollution.png')
plt.show()


window_size = 5 # 滑动窗口大小
max_points = 365 # 准备做时序分解时候的大小
fill_points = 10 # 预测未来数据的数目



# Decomposing our time series
# Seasonal-Trend-Loss
# Model
# y(t) = Trend + Seasonality + Residual
# series = air_pollution.pollution_today[:365]
# result = seasonal_decompose(series, model='multiplicative')
# result.plot()
#
# plt.savefig('pollution_today.png')
# plt.show()


