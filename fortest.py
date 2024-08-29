import pandas as pd
from datetime import datetime, timedelta

# 원본 데이터를 읽어옵니다. (CSV 파일이라고 가정)
# 실제 파일 경로로 변경해야 합니다.
df = pd.read_csv('min_rb_per_cell_time_entropy_zero_results.csv')

# 2024년 4월 1일부터 7일까지의 날짜와 시간 생성 (15분 간격)
start_date = datetime(2024, 4, 1)
end_date = datetime(2024, 4, 7, 23, 45)  # 4월 7일 23:45까지
date_range = pd.date_range(start=start_date, end=end_date, freq='15min')

# 새로운 데이터프레임 생성
new_data = []
for enbid_pci in df['enbid_pci'].unique():
    df_enbid = df[df['enbid_pci'] == enbid_pci]
    for timestamp in date_range:
        day_time = timestamp.strftime('%H:%M')
        matching_row = df_enbid[df_enbid['time'] == day_time]
        if not matching_row.empty:
            new_row = matching_row.iloc[0].copy()
            new_row['timestamp'] = timestamp.strftime('%Y-%m-%d %H:%M')
            new_data.append(new_row)

new_df = pd.DataFrame(new_data)

# timestamp 열을 첫 번째 열로 이동
columns = ['timestamp'] + [col for col in new_df.columns if col != 'timestamp']
new_df = new_df[columns]

# 결과 출력 (처음 10행과 마지막 10행)
print(new_df.head(10).to_string(index=False))
print("\n...(중략)...\n")
print(new_df.tail(10).to_string(index=False))
print(f"\n총 행 수: {len(new_df)}")

# 결과를 CSV 파일로 저장 (선택사항)
new_df.to_csv('data_with_timestamp_april1-7.csv', index=False)