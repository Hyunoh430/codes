import pandas as pd

# CSV 파일에서 데이터 로드
df = pd.read_csv('sleep_possibilities_combined.csv', parse_dates=['timestamp'])

# timestamp와 enbid_pci 기준으로 오름차순 정렬
df_sorted = df.sort_values(by=['timestamp', 'enbid_pci'])

# 정렬된 데이터프레임을 확인하기 위해 상위 몇 개 행 출력
print(df_sorted.head())

# 정렬된 데이터프레임을 새로운 CSV 파일로 저장
df_sorted.to_csv('sleep_sorted_enbid_pci_data.csv', index=False)
