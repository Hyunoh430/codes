import pandas as pd

# CSV 파일에서 데이터 로드
df = pd.read_csv('enbid_pci_sorted_data.csv', parse_dates=['timestamp'])

# timestamp 열을 datetime 형식으로 변환하고 time과 date 열 추가
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['time'] = df['timestamp'].dt.time
df['date'] = df['timestamp'].dt.date

# 주파수 대역 컬럼 리스트 정의
RB_columns = ['RB_800', 'RB_1800', 'RB_2100', 'RB_2600_10', 'RB_2600_20']

# 각 주파수 대역의 최대 가용 RB 수 정의
max_rb = {'RB_800': 50, 'RB_1800': 100, 'RB_2100': 75, 'RB_2600_10': 50, 'RB_2600_20': 100}

def check_sleep_possibility(row, band):

    adjusted_rbtotal = row['RBtotal'] - max_rb[band]
    threshold = 0.6 * adjusted_rbtotal
    return int(row['RBused'] <= threshold)

# 각 주파수 대역별로 슬립 가능성 계산
for band in RB_columns:
    df[f'sleep_possible_{band}'] = df.apply(lambda row: check_sleep_possibility(row, band), axis=1)

# 결과를 CSV 파일로 저장
output_file = 'sleep_possibilities_combined.csv'
df.to_csv(output_file, index=False, columns=['timestamp', 'enbid_pci'] + [f'sleep_possible_{band}' for band in RB_columns])

print(f"All processing completed. Results saved in '{output_file}'.")
print(df[['timestamp', 'enbid_pci'] + [f'sleep_possible_{band}' for band in RB_columns]].head())  # 결과 확인을 위해 상위 몇 개 행 출력

