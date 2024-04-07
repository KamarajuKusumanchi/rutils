#! /usr/bin/env python3
import pandas as pd
import sys
df = pd.read_csv(sys.stdin, dtype='str')
mask = (df['nag_name'] == 'blunder') | (df['nag_name'] == 'mistake')
df = df[mask]
df['variation'] = df['best_move']
df.to_csv(sys.stdout, index=False, header=False)
