import pandas as pd

# CSV 데이터 로드
file_path = 'enbid_pci_sorted_data.csv'
df = pd.read_csv(file_path)

print(df.head(5))