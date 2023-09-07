import module as md
import os
import pandas as pd
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

# 기본 데이터 전처리

path = os.path.dirname(__file__)
file_path = path + '\\\\data\\\\'
font_path = file_path + 'NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path)

df_main = pd.read_csv(file_path + 'SURFACE_ASOS_108_MI_2023-08_2023-08_2023.csv', encoding='euc-kr')
df_main.fillna(np.nan, inplace=True)		# 결측치 to np.nan
df_main['일시'] = pd.to_datetime(df_main['일시'])	# '일시' 열 타입 변환
df_main.set_index('일시', inplace=True) # '일시' 열 인덱스화

df_main = df_main[:'2023-08-20']	# 8월 1일 ~ 8월 20일
df = df_main.copy()
df.rename(columns={'기온(°C)':'기온(섭씨)'}, inplace=True)	# 칼럼 쓰기 쉽게 변환
df = md.diffError(df, '기온(섭씨)') # 분별 온도차가 3도를 넘는경우 np.nan 처리
df = md.diffSumError(df, '기온(섭씨)') # 시간마다 분별 온도차의 합이 0.1보다 작은 경우 np.nan 처리

# 80% 확인 후 보간
df_original = df.copy() # 보간 전 데이터( == 결측값 보유한 데이터)
df_itp = md.checkData(df)   # 보간 후 데이터

# 밤낮 평균 온도 구하기

df_day = md.groupDay(df_itp, 'day')

def monthstemp():
    df_day_gpd = df_day['기온(섭씨)'].groupby(df_day['day']).agg(['mean', 'max', 'min'])
    return df_day_gpd

def hourmeantemp():
    df_itp['시간'] = df_itp.index.hour
    df_hour_mean = pd.DataFrame(df_itp['기온(섭씨)'].groupby(df_itp['시간']).mean())
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df_hour_mean.index, df_hour_mean['기온(섭씨)'])
    ax.set_title('8월1일~8월20일 시간별 평균 기온',fontproperties=fontprop, fontsize=15)
    ax.set_xticks(df_hour_mean.index)
    ax.set_xlabel('시간', fontproperties=fontprop, fontsize=13)
    ax.set_ylabel('기온', fontproperties=fontprop, fontsize=13)
    return fig
# 월간 일일 낮, 아침 온도 비교 (이유:평균 온도가 아침이 제일 낮고, 낮이 제일 높아서)
df_dawn, df_morning, df_daytime, df_evening, df_night = md.makedaydf(df_day)

def dailytemp():
    fig = plt.figure(figsize = (10,8))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(df_dawn.index, df_dawn['기온(섭씨)'], label='새벽')
    ax1.plot(df_morning.index, df_morning['기온(섭씨)'], label='아침')
    ax1.plot(df_daytime.index, df_daytime['기온(섭씨)'], label='낮')
    ax1.plot(df_evening.index, df_evening['기온(섭씨)'], label='저녁')
    ax1.plot(df_night.index, df_night['기온(섭씨)'], label='밤')
    ax1.legend(loc='lower left', prop=fontprop)
    ax1.set_title('시간대별 평균 기온', fontproperties=fontprop, fontsize=15)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(df_morning.index, df_morning['기온(섭씨)'], color='orange', label='아침')
    ax2.plot(df_daytime.index, df_daytime['기온(섭씨)'], color='green', label='낮')
    ax2.legend(prop=fontprop)
    ax2.set_title('낮-아침 평균 기온', fontproperties=fontprop, fontsize=15)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    fig.subplots_adjust(hspace=0.5)
    
    max_daytime = df_daytime['기온(섭씨)'].max()
    min_daytime = df_daytime['기온(섭씨)'].min()
    max_morning = df_morning['기온(섭씨)'].max()
    min_morning = df_morning['기온(섭씨)'].min()
    ax2.plot(df_morning['기온(섭씨)'].idxmax(), max_morning, 'ro')
    ax2.annotate(f'{max_daytime:.2f}', xy=(df_morning['기온(섭씨)'].idxmax(), max_morning), fontsize=10, xytext=(0, -50),
             textcoords='offset points', arrowprops=dict(arrowstyle='->', color='red'))
    ax2.plot(df_morning['기온(섭씨)'].idxmin(), min_morning, 'ro')
    ax2.annotate(f'{min_daytime:.2f}', xy=(df_morning['기온(섭씨)'].idxmin(), min_morning), fontsize=10, xytext=(0, 60),
             textcoords='offset points', arrowprops=dict(arrowstyle='->', color='red'))
    
    ax2.plot(df_daytime['기온(섭씨)'].idxmax(), max_daytime, 'ro')
    ax2.annotate(f'{max_daytime:.2f}', xy=(df_daytime['기온(섭씨)'].idxmax(), max_daytime), fontsize=10, xytext=(50, -10),
             textcoords='offset points', arrowprops=dict(arrowstyle='->', color='red'))
    ax2.plot(df_daytime['기온(섭씨)'].idxmin(), min_daytime, 'ro')
    ax2.annotate(f'{min_daytime:.2f}', xy=(df_daytime['기온(섭씨)'].idxmin(), min_daytime), fontsize=10, xytext=(-50, 0),
             textcoords='offset points', arrowprops=dict(arrowstyle='->', color='red'))
    return fig


# 80% 확인 후 보간
df_original = df.copy() # 보간 전 데이터( == 결측값 보유한 데이터)
df_itp = md.checkData(df)   # 보간 후 데이터

# 그래프
df_original_hour_gpd = df_original.resample('H').agg(['mean', 'max', 'min'])
df_itp_hour_gpd = df_itp.resample('H').agg(['mean', 'max', 'min'])
df_original_day_gpd = df_original.resample('D').agg(['mean', 'max', 'min'])
df_itp_day_gpd = df_itp.resample('D').agg(['mean', 'max', 'min'])

df_1H = df_itp['기온(섭씨)'].rolling('H').mean()
df_1H_gpd = df_1H.resample('D').mean()
df_3H = df_itp['기온(섭씨)'].rolling('3H').mean()
df_3H_gpd = df_3H.resample('D').mean()
df_8H = df_itp['기온(섭씨)'].rolling('8H').mean()
df_8H_gpd = df_8H.resample('D').mean()
df_1DAY = df_itp['기온(섭씨)'].rolling('D').mean()
df_1DAY_gpd = df_1DAY.resample('D').mean()

def hourgraph():				# 시간별 기온, 강수량, 풍속 그래프
    fig = plt.figure(figsize=(10,8))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(df_original_hour_gpd.index, df_original_hour_gpd['기온(섭씨)']['mean'], label='기온(섭씨)')
    ax1.plot(df_original_hour_gpd.index, df_original_hour_gpd['누적강수량(mm)']['mean'], label='누적 강수량(mm))')
    ax1.plot(df_original_hour_gpd.index, df_original_hour_gpd['풍속(m/s)']['mean'], label='풍속(m/s)')
    ax1.legend(loc='best', prop=fontprop)
    ax1.set_title('시간별 기온', fontproperties=fontprop) 

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(df_itp_hour_gpd.index, df_itp_hour_gpd['기온(섭씨)']['mean'], label='기온(섭씨)')
    ax2.plot(df_itp_hour_gpd.index, df_itp_hour_gpd['누적강수량(mm)']['mean'], label='누적 강수량(mm))')
    ax2.plot(df_itp_hour_gpd.index, df_itp_hour_gpd['풍속(m/s)']['mean'], label='풍속(m/s)')
    ax2.legend(loc='best', prop=fontprop)
    ax2.set_title('시간별 기온 - 보간', fontproperties=fontprop)
    return fig

def dailygraph():				# 일일 기온, 강수량, 풍속 그래프
    fig = plt.figure(figsize=(10,8))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(df_original_day_gpd.index, df_original_day_gpd['기온(섭씨)']['mean'], label='기온(섭씨)')
    ax1.plot(df_original_day_gpd.index, df_original_day_gpd['누적강수량(mm)']['mean'], label='누적 강수량(mm))')
    ax1.plot(df_original_day_gpd.index, df_original_day_gpd['풍속(m/s)']['mean'], label='풍속(m/s)')
    ax1.legend(loc='best', prop=fontprop)
    ax1.set_title('일별 기온', fontproperties=fontprop) 
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(df_itp_day_gpd.index, df_itp_day_gpd['기온(섭씨)']['mean'], label='기온(섭씨)')
    ax2.plot(df_itp_day_gpd.index, df_itp_day_gpd['누적강수량(mm)']['mean'], label='누적 강수량(mm))')
    ax2.plot(df_itp_day_gpd.index, df_itp_day_gpd['풍속(m/s)']['mean'], label='풍속(m/s)')
    ax2.legend(loc='best', prop=fontprop)
    ax2.set_title('일별 기온 - 보간', fontproperties=fontprop)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    fig.subplots_adjust(hspace=0.5)
    return fig

def meangraph():    # 1시간,3시간,8시간,1일 동안의 평균 기온
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df_1H_gpd.index, df_1H_gpd.values, label = '1시간')
    ax.plot(df_3H_gpd.index, df_3H_gpd.values, label = '3시간')
    ax.plot(df_8H_gpd.index, df_8H_gpd.values, label = '8시간')
    ax.plot(df_1DAY_gpd.index, df_1DAY_gpd.values, label = '1일')
    ax.legend(prop=fontprop)
    ax.set_title('평균 기온', fontproperties=fontprop, fontsize=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_ylabel('기온', fontproperties=fontprop, rotation=0, fontsize=13)
    return fig

