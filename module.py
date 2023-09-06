# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:19:46 2023

@author: rnjsd
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime



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

def toDateTime(val):
    return datetime.strptime(val, '%Y-%m-%d %H:%M')

def addDayNight(df, day):
    df_index = df.index.hour.unique()
    for hour in df_index:
        for day_, hour_ in day.items():
            if hour in hour_:
                df.loc[df.index.hour == hour, 'DAY'] = day_
    return df

