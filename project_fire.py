import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv('data/fire.csv')
df
df.columns

# 커밋 테스트트
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

#변수명 변경
data=data.rename(columns={'항목':'month'})
data=data.rename(columns={'계':'total'})
data=data.rename(columns={'전기적요인':'electrical'})
data=data.rename(columns={'기계적요인':'mechanical'})
data=data.rename(columns={'화학적요인':'chemical'})
data=data.rename(columns={'가스누출':'gas'})
data=data.rename(columns={'교통사고':'Traffic'})
data=data.rename(columns={'부주의':'Negligence'})
data=data.rename(columns={'기타':'other'})
data=data.rename(columns={'자연적요인':'natural'})
data=data.rename(columns={'방화':'arson'})
data=data.rename(columns={'방화의심':'suspected'})
data=data.rename(columns={'미상':'unknown'})
data

# for문 사용하여 전체 열을 int로 변환
data.info()
columns_to_convert = ['total', 'electrical', 'mechanical', 'chemical',
                      'gas', 'Traffic', 'Negligence', 'other', 'natural',
                      'arson', 'suspected', 'unknown']

for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column])
    
data.info()

# 계절 파생변수 추가
data['season']=np.where(data['month'].isin(['12월','1월','2월']),'winter',
             np.where(data['month'].isin(['3월','4월','5월']),'spring',
             np.where(data['month'].isin(['6월','7월','8월']),'summer','fall')))

# 계절 순서를 봄, 여름, 겨울, 가을로 설정
order = ['spring', 'summer', 'fall', 'winter']
data['season'] = pd.Categorical(data['season'], categories=order, ordered=True)
data = data.sort_values(['year', 'season'])
data

# 계절별 화재 발생횟수 데이터프레임 생성
season=data.groupby(['year','season']).agg(n=('total','sum'))
season

#선그래프 생성
sns.lineplot(data=season ,x='season', y='n', hue='year',
             marker='o', markersize=10)

plt.title('Seasonal Fire Incidents')
plt.xlabel('Season')
plt.ylabel('Number of Incidents')

plt.show()
plt.clf()

#연도별 평균 데이터 시리즈
data
data_mean = (data[columns_to_convert].sum()/3).drop('total')
data_mean

# 막대그래프 생성
data_mean.plot(kind='bar')

plt.title('Yearly Average of Fire Incident Causes')
plt.xlabel('Cause of Fire')
plt.ylabel('Mean Value')
plt.xticks(rotation=45)
plt.tight_layout()

# 그래프 보여주기
plt.show()
plt.clf()
