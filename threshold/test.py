import pandas as pd
import numpy as np
from datetime import datetime, timedelta

df = pd.read_csv('ELG_Busan_PoC_per_CA_site_0226_0407.csv')

print(df.iloc[0])