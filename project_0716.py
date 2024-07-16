import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 데이터 정리
df = pd.read_csv("fire.csv")
df
df.columns

# 2020년도만 뽑아오기
data_2020 = df[['행정구역별'] + df.filter(like='2020').columns.tolist()]
data_2020

data_2020.columns = data_2020.iloc[0] #0번째 행을 열로
data_2020

data_2020 = data_2020[1:]
data_2020 = data_2020.reset_index(drop=True)
data_2020

data_2020_pop = data_2020.iloc[:, 0:4]
data_2020_pop

data_2020_pop.columns

pop = data_2020_pop.copy()
pop

pop.info() # 데이터타입 확인

# 문자형을 숫자형으로 변환
pop['건수 (건)'] = pd.to_numeric(pop['건수 (건)'])
pop['사망 (명)'] = pd.to_numeric(pop['사망 (명)'])
pop['부상 (명)'] = pd.to_numeric(pop['부상 (명)'])


# 변수명 변경
pop = pop.rename(columns = {"건수 (건)" : "건수"})
pop = pop.rename(columns = {"사망 (명)" : "사망자수"})
pop = pop.rename(columns = {"부상 (명)" : "부상자수"})

# 건수별로 정렬 
pop.sort_values("건수", ascending = False)

# 인명 피해
pop["total"] = pop["사망자수"] + pop["부상자수"]
pop.head()

# 위험도 추가
count_mean = 38659/17  #평균
pop["위험도"] = np.where(pop["건수"] >= count_mean, "dan", "saf")
pop.head()

# 빈도 막대 그래프
pop["위험도"].value_counts().plot.bar(rot=0) #rot=0 : 축 이름 수평
plt.show()
plt.clf()

# 시도별 인명피해 그래프
pop["total"].plot.bar(rot = 0)
plt.show()
