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

df_main = pd.read_csv(file_path + '산업통상자원부_반도체디스플레이 수출동향 추이_20221231.csv')
df = df_main.copy()
df['년월'] = pd.to_datetime(df['년월'])
df.set_index('년월', inplace=True)
df_year = df.resample('Y').sum()

# 그래프

fig = md.sidexport(df_year) # 반도체 수출(각 항목의 비율 표시)
plt.show()


fig = md.exportplot(df_year, '반도체(억불)', '메모리(억불)', '시스템_반도체(억불)')
plt.show()  # 반도체 + 메모리 + 비 메모리 수출

fig = md.memoryratio(df_year)
plt.show()


