
import numpy as np
import pandas as pd

def make_order2_interactions(df: pd.DataFrame):
    df2 = df.copy()
    for c1 in df.columns:
        for c2 in df.columns:
            df2[f"{c1}_{c2}"] = df[c1] * df[c2]
    return df2

def make_order3_interactions(df: pd.DataFrame):
    df2 = df.copy()
    for c1 in df.columns:
        for c2 in df.columns:
            for c3 in df.columns:
                df2[f"{c1}_{c2}_{c3}"] = df[c1] * df[c2] * df[c3]
    return df2

def make_interactions(df: pd.DataFrame, order=2):
    assert order in [2,3]
    if order == 2: 
        return make_order2_interactions(df)
    else: 
        return make_order3_interactions(df) 

