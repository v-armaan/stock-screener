import pandas as pd
import numpy as np
import yfinance as yf
def data_clean(df):
    """
    to drop rows with a majority of NaN values and remove duplicate rows
    parameters:df pandas.DataFrame
    returns:final_df pandas.DataFrame
    1)drop data rows with NaN in Close values
    2)only OHLCV values matter so drop a row if majority of those are NaN
    3)take rows from ohlcv cleaned data and select only thsoe rows from df
    3)handle duplicates later
    """
    ##dropping Close NaN rows
    df=df.drop(df.index[df["Close"].isna()])
    ##dropping rows with 3 or more/5 NaN values in a row in ohlcv
    ohlcv=df[["Open","High","Low","Close","Volume"]]
    rows_to_drop=[]#cannot drop rows from original database in loop  because then the index positions change
    for i in range(len(ohlcv)):
        if (ohlcv.iloc[i,:].isna().sum())>=3:
            rows_to_drop.append(ohlcv.index[i])
    ohlcv.drop(rows_to_drop,inplace=True)
    ##eliminating row indexes from df which arent present in ohlcv
    rows_to_drop_indf=[]
    for i in range(len(df.index)):
        if (df.index[i] not in ohlcv.index):
            rows_to_drop_indf.append(df.index[i])
    df.drop(rows_to_drop_indf,inplace=True) 
    return(df)
    

# #testing
# df=yf.Ticker("AAPL").history(period="1y")
# bad_df = df.copy()

# # 1 Close NaN
# bad_df.loc[bad_df.index[5], "Close"] = np.nan

# # 2 NaNs in the OHLCV columns
# bad_df.loc[bad_df.index[10], ["Open", "High", "Low"]] = np.nan

# # 3 Another row with 3 NaNs
# bad_df.loc[bad_df.index[15], ["Open", "Close", "Volume"]] = np.nan

# cleaned_df=data_clean(bad_df)
# print(cleaned_df.isna().sum(),"\n\n")
