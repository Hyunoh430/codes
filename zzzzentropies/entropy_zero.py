import pandas as pd
import numpy as np

# CSV 파일에서 데이터 로드
df = pd.read_csv('sleep_probabilities_result.csv')

# 엔트로피 계산 함수
def calculate_entropy(p):
    # 0과 1을 피하기 위해 아주 작은 값을 더하거나 뺍니다
    p = np.clip(p, 1e-10, 1 - 1e-10)
    entropy = -p * np.log2(p) - (1-p) * np.log2(1-p)
    # 매우 작은 엔트로피 값을 0으로 변환
    return 0 if entropy < 1e-6 else entropy

# 주파수 대역 컬럼 리스트
RB_columns = ['sleep_probability_RB_800', 'sleep_probability_RB_1800', 
              'sleep_probability_RB_2100', 'sleep_probability_RB_2600_10', 
              'sleep_probability_RB_2600_20']

# 각 enbid_pci와 시간대별로 엔트로피 계산
entropy_results = []

for enbid_pci in df['enbid_pci'].unique():
    enbid_data = df[df['enbid_pci'] == enbid_pci]
    
    for time in enbid_data['time'].unique():
        time_data = enbid_data[enbid_data['time'] == time]
        
        total_entropy = 0
        for band in RB_columns:
            if not pd.isna(time_data[band].iloc[0]):  # NaN 값 체크
                band_entropy = calculate_entropy(time_data[band].iloc[0])
                total_entropy += band_entropy
        
        # 총 엔트로피가 매우 작은 경우 0으로 설정
        total_entropy = 0 if total_entropy < 1e-6 else total_entropy
        
        entropy_results.append({
            'enbid_pci': enbid_pci,
            'time': time,
            'total_entropy': total_entropy
        })

# 결과를 DataFrame으로 변환
entropy_df = pd.DataFrame(entropy_results)

# 시간순으로 정렬
entropy_df['time'] = pd.to_datetime(entropy_df['time']).dt.time
entropy_df = entropy_df.sort_values(['enbid_pci', 'time'])

# 결과 출력 (처음 몇 행만)
print(entropy_df.head(20))

# CSV 파일로 저장
entropy_df.to_csv('222entropy_results_by_enbid_pci.csv', index=False)