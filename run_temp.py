import temp
import matplotlib.pyplot as plt

df_day_gpd = temp.monthstemp() # 8월1일~8월20일 시간대별 평균, 최대, 최소 기온
print(df_day_gpd)  
fig = temp.hourmeantemp()
plt.show()

fig = temp.dailytemp()
plt.show()

df_count = temp.md.printcheckData(temp.df)  # 각 시간이 가지고있는 분별데이터가 80% 이하인 경우만 표출
print(df_count)


fig = temp.hourgraph()
plt.show()

fig = temp.dailygraph()
plt.show()

fig = temp.meangraph()
plt.show()



