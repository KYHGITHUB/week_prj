# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:19:46 2023

@author: rnjsd
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import font_manager as fm

path = os.path.dirname(__file__)
file_path = path + '\\\\data\\\\'
font_path = file_path + 'NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path)

def diff(df, column):
    result_df = df[column].diff().abs()
    return result_df

def diffError(df, column):
    df_diff = diff(df, column)
    for date in df_diff.index:
        if df_diff.loc[date] > 3:
            df.loc[date, column] = np.nan
    return df

def diffSumError(df,column):
    df_diff = diff(df, column)
    error = df_diff.resample('H').sum()[df_diff.resample('H').sum() < 0.1]
    for i in range(len(error)):
        df.loc[str(error.index[i])[:-6]].loc[:, column] = np.nan
    return df

def toNan(df):
    df.fillna(np.nan, inplace=True)
    return df

def groupDay(df, new_column):
    df_copy = df.copy()
    df_copy[new_column] = pd.cut(df_copy.index.hour,
       bins = [0, 4, 8, 16, 20, 23],
       labels = ['새벽', '아침', '낮', '저녁', '밤'],
       include_lowest=True)
    return df_copy

def checkData(df):
    df_copy = df.copy()
    mask = df_copy['기온(섭씨)'].resample('H').count() < 60*0.8
    df_count = df_copy.resample('H').count()[mask]
    if df_count.empty:
        pass
    else:
        df_copy.loc[:,:'일조(Sec)'] = df_copy.loc[:,:'일조(Sec)'].interpolate(method='linear')
    return df_copy

def printcheckData(df):
    df_copy = df.copy()
    mask = df_copy['기온(섭씨)'].resample('H').count() < 60*0.8
    df_count = df_copy.resample('H').count()[mask]
    return df_count

def makedaydf(df):
    day_list = ['새벽', '아침', '낮', '저녁', '밤']
    for day in day_list:
        mask = df['day'] == day
        if day == '새벽':
            df_dawn = df.loc[:,:'일조(Sec)'][mask].resample('D').mean()
        elif day == '아침':
            df_morning = df.loc[:,:'일조(Sec)'][mask].resample('D').mean()
        elif day == '낮':
            df_daytime = df.loc[:,:'일조(Sec)'][mask].resample('D').mean()
        elif day == '저녁':
            df_evening = df.loc[:,:'일조(Sec)'][mask].resample('D').mean()
        else:
            df_night = df.loc[:,:'일조(Sec)'][mask].resample('D').mean()
    return df_dawn, df_morning, df_daytime, df_evening, df_night

def sidexport(df):
    n_df = df.copy()
    year_list = n_df.index.year.tolist()
    sid_dict = {}
    for column in n_df.loc[:,['메모리(억불)', '시스템_반도체(억불)', '개별소자(억불)']].columns:
        sid_dict[column] = n_df[column].values
        
    width = 0.5  # the width of the bars: can also be len(x) sequence


    fig, ax = plt.subplots()
    bottom = np.zeros(len(sid_dict['메모리(억불)']))

    for key, value in sid_dict.items():
        p = ax.bar(year_list, value, width, label=key[:-4], bottom=bottom)
        bottom += value

        ax.bar_label(p, label_type='center')

    ax.set_title('반도체 수출', fontproperties=fontprop, fontsize=15)
    ax.legend(prop=fontprop)
    ax.set_ylabel('억불', fontproperties=fontprop, rotation=0)
    return fig
    
def exportplot(df, *args):
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(df.index.year, df[list(args)].values, label=list(args))
    ax.legend(prop=fontprop)
    ax.set_title('반도체(메모리+시스템) 수출', fontproperties=fontprop, fontsize = 15)
    return fig


def memoryratio(df):
    n_df = df.copy()
    n_df['메모리_D램 비율'] = n_df['메모리_D램(억불)'] / n_df['메모리(억불)'] * 100
    n_df['메모리_낸드 비율'] = n_df['메모리_낸드(억불)'] / n_df['메모리(억불)'] * 100
    n_df['메모리_MCP 비율'] = n_df['메모리_MCP(억불)'] / n_df['메모리(억불)'] * 100
    n_df['기타'] = 100 - n_df['메모리_D램 비율'] - n_df['메모리_낸드 비율'] - n_df['메모리_MCP 비율']
    columns_list = list(n_df.columns[-4:])
    export_dict = {}
    for year in n_df.index.year:
        export_dict[year]= n_df.loc[str(year)].loc[:, columns_list].values[0].tolist()
    
    labels = list(export_dict.keys())
    data = np.array(list(export_dict.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(columns_list, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname.split(' ')[0], color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncols=len(columns_list), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small', prop=fontprop)
    return fig
    