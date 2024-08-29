import pandas as pd
import os

# CSV 파일 읽기
df = pd.read_csv('ELG_Busan_PoC_per_CA_site_0226_0407.csv')  # 'your_file.csv'를 실제 파일 이름으로 변경하세요

# 관심있는 열들
columns_of_interest = ['Equip_800', 'Equip_1800', 'Equip_2100', 'Equip_2600_10', 'Equip_2600_20']

# 고유한 조합을 찾고 각 조합에 대해 새 파일 생성
for i, group in df.groupby(columns_of_interest):
    # 조합을 문자열로 변환
    combination = '_'.join(map(str, i))
    
    # 새 파일 이름 생성
    new_filename = f'combination_{combination}.csv'
    
    # 중복된 파일 이름 방지
    counter = 1
    while os.path.exists(new_filename):
        new_filename = f'combination_{combination}_{counter}.csv'
        counter += 1
    
    # 그룹을 새 CSV 파일로 저장
    group.to_csv(new_filename, index=False)
    print(f'파일 저장됨: {new_filename}')

print('모든 파일이 저장되었습니다.')