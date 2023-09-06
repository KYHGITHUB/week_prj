import module as md
import os
import pandas as pd
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

# 기본 데이터 전처리

path = os.path.dirname(__file__)
file_path = path + '\\\\data\\\\'
df_main = pd.read_csv(file_path + 'SURFACE_ASOS_108_MI_2023-08_2023-08_2023.csv', encoding='euc-kr')
df_main.fillna(np.nan, inplace=True)		# 결측치 to np.nan
df_main['일시'] = pd.to_datetime(df_main['일시'])	# '일시' 열 타입 변환
df_main.set_index('일시', inplace=True) # '일시' 열 인덱스화

df_main = df_main[:'2023-08-20']	# 8월 1일 ~ 8월 20일
df = df_main.copy()
df.rename(columns={'기온(°C)':'기온(섭씨)'}, inplace=True)	# 칼럼 쓰기 쉽게 변환
df = md.diffError(df, '기온(섭씨)') # 분별 온도차가 3도를 넘는경우 np.nan 처리
df = md.diffSumError(df, '기온(섭씨)') # 시간마다 분별 온도차의 합이 0.1보다 작은 경우 np.nan 처리

df_drop = df.dropna(subset='기온(섭씨)')

# 밤낮 평균 온도 구하기

df_day = md.groupDay(df, 'day')

def DayNight():
    gpd_df_day = df_day['기온(섭씨)'].groupby(df_day['day']).mean()
    return gpd_df_day

# 80% 확인
def checkData():
    df_count = df['기온(섭씨)'].resample('D').count()
    mask = df_count < 1440*0.8	# 1일 = 1440분
    if df_count[mask].empty:
        print('사용가능한 데이터 입니다.')
    else:
        print('보간 작업이 필요합니다.')
    #return df_count[mask]	# gap filling 해야하는 시간대 확인

# 그래프

font_path = file_path + 'NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path, size=15)
gpd_df_graph = df_drop.resample('D').agg(['mean', 'max', 'min'])

# 결측값 채우지 않고
def NoGap():
    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(gpd_df_graph.index, gpd_df_graph['기온(섭씨)']['mean'], label='기온(섭씨)')
    ax.plot(gpd_df_graph.index, gpd_df_graph['누적강수량(mm)']['mean'], label='누적 강수량(mm))')
    ax.plot(gpd_df_graph.index, gpd_df_graph['풍속(m/s)']['mean'], label='풍속(m/s)')
    ax.legend(loc='best', prop=fontprop)
    ax.set_xlabel('날짜', fontproperties=fontprop)
    return fig

# 결측값 채우고
def Gap():
    fig = plt.figure(figsize=(12,6))
    df_gap = df.interpolate(method='linear')
    gpd_df_gap = df_gap.resample('D').agg(['mean', 'max', 'min'])
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(gpd_df_gap.index, gpd_df_gap['기온(섭씨)']['mean'], label='기온(섭씨)')
    ax.plot(gpd_df_gap.index, gpd_df_gap['누적강수량(mm)']['mean'], label='누적 강수량(mm))')
    ax.plot(gpd_df_gap.index, gpd_df_gap['풍속(m/s)']['mean'], label='풍속(m/s)')
    ax.legend(loc='best', prop=fontprop)
    ax.set_xlabel('날짜', fontproperties=fontprop)
    return fig

def check():
    
    print(len(df_drop) >= len(df['기온(섭씨)'])*0.8)