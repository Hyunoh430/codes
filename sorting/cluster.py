import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# 데이터 로드 (예시)
data = pd.read_csv('ELG_Busan_PoC_per_CA_site_0226_0407.csv')

# 특성 추출 (15분 간격 데이터, 주말 고려 제거)
def extract_features(data):
    # 'timestamp'에서 15분 간격으로 시간대를 계산
    data['time_interval'] = pd.to_datetime(data['timestamp']).dt.floor('15min')
    
    features = pd.DataFrame()
    features['enbid_pci'] = data['enbid_pci'].unique()

    # 15분 간격의 RB 사용량 평균
    rb_usage_avg = data.groupby(['enbid_pci', 'time_interval'])['RBused'].mean().unstack(fill_value=0)
    rb_usage_avg.columns = [f'rb_usage_{col.time()}' for col in rb_usage_avg.columns]
    features = features.join(rb_usage_avg, on='enbid_pci')

    # 피크 시간대 RB 사용량 (15분 간격으로 고려)
    features['peak_interval_usage'] = data.groupby('enbid_pci')['RBused'].max()

    # 주파수 대역별 사용 비율
    for rb in ['RB_800', 'RB_1800', 'RB_2100', 'RB_2600_10', 'RB_2600_20']:
        features[f'{rb}_ratio'] = data.groupby('enbid_pci')[rb].mean() / data.groupby('enbid_pci')['RBused'].mean()

    # RB 사용량의 변동성 (15분 간격 데이터의 변동성)
    features['rb_usage_std'] = data.groupby('enbid_pci')['RBused'].std()

    return features

features = extract_features(data)

# 결측값을 0으로 대체
features.fillna(0, inplace=True)

# 정규화
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features.drop('enbid_pci', axis=1))

# PCA
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_features)

# K-means 클러스터링
kmeans = KMeans(n_clusters=5, random_state=42)
cluster_labels = kmeans.fit_predict(scaled_features)

# 시각화
plt.figure(figsize=(12, 8))
scatter = plt.scatter(pca_result[:, 0], pca_result[:, 1], c=cluster_labels, cmap='viridis')
plt.title('Clustered Regions based on Telecom Data')
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.colorbar(scatter)
plt.show()

# 클러스터 특성 분석
for cluster in range(5):
    cluster_data = features[cluster_labels == cluster]
    print(f"Cluster {cluster} characteristics:")
    print(cluster_data.mean())
    print("\n")
