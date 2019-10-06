import os
from glob import glob
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(BASE, 'data', 'raw_frames')

g = glob(os.path.join(DIR, '*'))

for path in g:
    df = pd.read_csv(os.path.join(path, 'vehicle.csv'))
    df['timestamp'] = df['timestamp'].astype(int)
    df.to_csv(os.path.join(path, 'vehicle.csv'), index=False)
    print(df.columns)
