#! /usr/bin/env python3
import pandas as pd
import sys
df = pd.read_csv(sys.stdin, dtype='str')
mask = (df['nag_name'] == 'blunder') | (df['nag_name'] == 'mistake')
df = df[mask]
df[['variation', 'best_move']] = df[['best_move', 'variation']]
df.to_csv(sys.stdout, index=False, header=False)
