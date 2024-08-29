import pandas as pd

# CSV 파일 읽기 (파일 경로를 적절히 수정해주세요)
df = pd.read_csv('sleep_possibilities_combined.csv')

# timestamp를 datetime 타입으로 변환
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 시간(HH:MM) 추출
df['time'] = df['timestamp'].dt.strftime('%H:%M')

# 주파수 대역 컬럼 리스트
frequency_bands = ['RB_800', 'RB_1800', 'RB_2100', 'RB_2600_10', 'RB_2600_20']

# enbid_pci와 time으로 그룹화하고 각 주파수 대역의 평균 계산
result = df.groupby(['enbid_pci', 'time']).agg({
    f'sleep_possible_{band}': 'mean' for band in frequency_bands
}).reset_index()

# 컬럼 이름 변경 (평균 값을 확률로 표시)
result.columns = ['enbid_pci', 'time'] + [f'sleep_probability_{band}' for band in frequency_bands]

# 결과 출력
print(result)

# CSV 파일로 저장 (선택사항)
result.to_csv('sleep_probabilities_result.csv', index=False)