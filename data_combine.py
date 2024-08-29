import pandas as pd

# 두 CSV 파일 읽기
df1 = pd.read_csv('ELG_Busan_PoC_per_CA_site_0226_0407.csv')
df2 = pd.read_csv('ELG_Busan_PoC_per_CA_site_0408_0519.csv')

# 두 데이터프레임 합치기
combined_df = pd.concat([df1, df2], ignore_index=True)

# 결과를 새 CSV 파일로 저장
combined_df.to_csv('ELG_Busan_PoC_per_CA_site_0226_0519.csv', index=False)

print("파일이 성공적으로 합쳐졌습니다.")