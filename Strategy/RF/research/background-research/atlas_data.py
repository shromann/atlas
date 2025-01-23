import pandas as pd
import numpy as np


def restructure(df):
    df = df.pivot(index='timestamp', columns='symbol', values=[col for col in df.columns if col not in ['symbol', 'timestamp']]).reset_index()
    df['date'] = df['timestamp'].dt.date    
    return df

def compute_log_returns(df, df_col):
    
    df[[f'LR_{sym}' for sym in df[df_col].columns]] = df[df_col][[sym for sym in df[df_col].columns]].map(np.log)

    for sym in df[df_col].columns:
        df[f'LR_{sym}'] = df.groupby('date')[f'LR_{sym}'].diff()

    return df
    
def log_return_impute(df, tkn='BTC/USD'):
    LR_syms = [f'LR_{sym}' for sym in df['close'].columns if tkn not in sym]
    # LR = df[LR_syms].droplevel(1, axis=1)
    iLR = df[f'LR_{tkn}']
    for LR_sym in LR_syms:
        df[LR_sym] = df[LR_sym].fillna(iLR)

    return df

def compute_volatility(df, sym='BTC/USD'):    
    df[f'sigmasq_{sym}'] = df[f'LR_{sym}'].map(np.square)
    return df
    
    
def get_features(df, tkn='BTC/USD'):
    df['dt'] = df.groupby('date_x')['timestamp'].diff().dt.seconds / 60

    # ts = df['timestamp']
    tc = df['trade_count'].add_prefix('trade_count_')
    vol = df['volume'].add_prefix('volume_')
    lr = (df[[col for col,_ in df.columns if 'LR_' in col]].droplevel(1, axis=1).T / df['dt']).T
    sg = df[f'sigmasq_{tkn}']

    return pd.concat([df['dt'], vol, tc, lr, sg], axis=1).fillna(0)

def process(etf_df, crypto_df):
    df = etf_df\
    .pipe(restructure)\
    .pipe(compute_log_returns, df_col='close')\
    .merge(
        crypto_df\
            .pipe(restructure)
            .pipe(compute_log_returns, df_col='close'), on='timestamp'
        )\
    .pipe(log_return_impute)\
    .pipe(compute_volatility)\
    .pipe(get_features)

    return df