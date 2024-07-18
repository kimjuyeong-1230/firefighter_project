import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

## 데이터 전처리

# 데이터 불러오기
df = pd.read_csv("C:/Data/발화요인에_대한_월별_화재발생현황.csv")
df
df.columns

# 연도별로 나눔
data_2020 = df[['항목'] + df.filter(like='2020').columns.tolist()]
data_2020

data_2021 = df[['항목'] + df.filter(like='2021').columns.tolist()]
data_2021

data_2022 = df[['항목'] + df.filter(like='2022').columns.tolist()]
data_2022

# 제품결함 제거
data_2022 = data_2022.drop(columns = "2022.11")
data_2022.columns

# 0번째 행을 열로 가져오기
data_2020.columns = data_2020.iloc[0] 
data_2020
data_2021.columns = data_2021.iloc[0] 
data_2021
data_2022.columns = data_2022.iloc[0] 
data_2022

# 합계부터 내용 가져오기
data_2020 = data_2020[2:]
data_2021 = data_2021[2:]
data_2022 = data_2022[2:]

# 인덱스 재정렬(리셋)
data_2020 = data_2020.reset_index(drop=True)
data_2021 = data_2021.reset_index(drop=True)
data_2022 = data_2022.reset_index(drop=True)

# year 변수 추가
data_2020['year']=2020
data_2021['year']=2021
data_2022['year']=2022

# 세로로 합치기
data = pd.concat([data_2020, data_2021, data_2022])
data

# 변환할 열 목록
columns_to_convert = ['계', '전기적요인', '기계적요인', '화학적요인', '가스누출', 
                      '교통사고', '부주의', '기타', '자연적요인', '방화', '방화의심', '미상']

# 각 열에 대해 pd.to_numeric 적용
for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column])
    
data.info()

# 파생 변수 만들기
data["계절"] = np.where(data["항목"].isin(["3월", "4월", "5월"]), "spring", 
               np.where(data["항목"].isin(["6월", "7월", "8월"]), "summer",
               np.where(data["항목"].isin(["9월", "10월", "11월"]), "fall", "winter")))
               
# 계절 순서 지정
data['계절'] = pd.Categorical(data['계절'], categories=["spring", "summer", "fall", "winter"], 
                              ordered=True)
                              
# 계절별 화재 발생횟수 데이터프레임 생성
seasonal_data = data.groupby(["year", "계절"]).agg(계절별화재 = ("계", "sum"))

# 그래프 시각화
plt.figure(figsize=(12, 6))
sns.lineplot(data = seasonal_data, x = "계절", y = "계절별화재", hue='year', marker='o')

plt.title('Seasonal Fire Incidents')
plt.xlabel('Season')
plt.ylabel('Number of Incidents')

plt.show()
plt.clf()
