import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv('data/fire.csv')
df
df.columns

# 년도별로 정리
data_2020 = df[['항목'] + df.filter(like='2020').columns.tolist()]
data_2020
data_2020.columns

data_2021 = df[['항목'] + df.filter(like='2021').columns.tolist()]
data_2021

data_2022 = df[['항목'] + df.filter(like='2022').columns.tolist()]
data_2022

# 제품결함 변수 제거
data_2022=data_2022.drop(columns = "2022.11")
data_2022

# 0행을 칼럼으로 지정
data_2020.columns = data_2020.iloc[0] 
data_2021.columns = data_2020.iloc[0] 
data_2022.columns = data_2020.iloc[0] 
data_2020
data_2021
data_2022

# 0,1행 제외하고 인덱스 초기화
data_2020 = data_2020[2:]
data_2020 = data_2020.reset_index(drop=True)
data_2020

data_2021 = data_2021[2:]
data_2021 = data_2021.reset_index(drop=True)
data_2021

data_2022 = data_2022[2:]
data_2022 = data_2022.reset_index(drop=True)
data_2022


# year 변수 추가
data_2020['year']=2020
data_2021['year']=2021
data_2022['year']=2022

# 세로로 합치기
data = pd.concat([data_2020, data_2021, data_2022])
data

# for문 사용하여 전체 열을 int로 변환
data.info()
columns_to_convert = ['계', '전기적요인', '기계적요인', '화학적요인',
                      '가스누출', '교통사고', '부주의', '기타', '자연적요인',
                      '방화', '방화의심', '미상']

for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column])
    
data.info()

# 계절 파생변수 추가
data['계절']=np.where(data['항목'].isin(['12월','1월','2월']),'winter',
             np.where(data['항목'].isin(['3월','4월','5월']),'spring',
             np.where(data['항목'].isin(['6월','7월','8월']),'summer','fall')))

# 계절 순서를 봄, 여름, 겨울, 가을로 설정
order = ['spring', 'summer', 'winter', 'fall']
data['계절'] = pd.Categorical(data['계절'], categories=order, ordered=True)
data = data.sort_values(['year', '계절'])
data

# 계절별 화재 발생횟수 데이터프레임 생성
season=data.groupby(['year','계절']).agg(계절별화재=('계','sum'))
season

#선그래프 생성
sns.lineplot(data=season ,x='계절', y='계절별화재', hue='year',
             marker='o', markersize=10)

plt.title('Seasonal Fire Incidents')
plt.xlabel('Season')
plt.ylabel('Number of Incidents')

plt.show()
plt.clf()

