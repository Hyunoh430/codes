import pandas as pd
import numpy as np

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['RB_usage'] = (df['RBused'].astype(float) / df['RBtotal'].astype(float)) * 100
    return df

def calculate_cv(group):
    return group.std() / group.mean() if group.mean() != 0 else 0

def analyze_variability(df):
    # 셀(enbid_pci)과 시간(hour)으로 그룹화
    grouped = df.groupby(['enbid_pci', 'hour'])['RB_usage']
    
    # 각 그룹(셀-시간)에 대해 CV 계산
    cv_df = grouped.apply(calculate_cv).reset_index(name='CV')
    return cv_df

def apply_threshold_rule(cv):
    if cv < 0.3:
        return 70
    elif cv < 0.5:
        return 65
    elif cv < 0.7:
        return 60
    else:
        return 55

def generate_results(cv_df):
    cv_df['threshold'] = cv_df['CV'].apply(apply_threshold_rule)
    results = cv_df.pivot(index='enbid_pci', columns='hour', values='threshold')
    return results

def save_results(results, output_file):
    new_columns = {i: f"{i:02d}:00-{i:02d}:59" for i in results.columns}
    results = results.rename(columns=new_columns)
    results.to_csv(output_file)
    print(f"\n결과 샘플:\n{results.head()}")

def main(input_file, output_file):
    df = load_and_preprocess_data(input_file)
    cv_df = analyze_variability(df)
    results = generate_results(cv_df)
    save_results(results, output_file)
    print(f"\n분석이 완료되었습니다. 결과가 {output_file}에 저장되었습니다.")

if __name__ == "__main__":
    input_file = "ELG_Busan_PoC_per_CA_site_0226_0407.csv"
    output_file = "rb_usage_hourly_thresholds2.csv"
    main(input_file, output_file)