"""
Calculations module for the stock screener.

This module calculates technical and price-based metrics from historical
OHLCV (Open, High, Low, Close, Volume) stock data.

The module includes functions for:
- Price metrics
- Moving averages (SMA and EMA)
- Momentum
- Relative Strength Index (RSI)
- Volume metrics, including RVOL and OBV
- Moving Average Convergence Divergence (MACD)
- Bollinger Bands
- Average True Range (ATR)
- 52-week high, low, and price distances

All functions accept a pandas DataFrame containing historical stock data
and return a pandas DataFrame containing the calculated metrics.
"""
import pandas as pd
import numpy as np

def calculate_price_metrics(df):
    """Calculate daily price changes, returns, range, and cumulative return (over the entire fetched period)."""
    price_metrics=pd.DataFrame()
    price_metrics["daily_change"]=df["Close"].diff()
    price_metrics["daily_return"]=df["Close"].pct_change()
    price_metrics["daily_range"]=df["High"]-df["Low"]
    price_metrics["cumulative_return"]=(df["Close"]-df["Close"].iloc[0])/(df["Close"].iloc[0])
    return(price_metrics)
def calc_1y_return(df):
    """Calculate price return over the trailing ~252 trading days (roughly 1 year), regardless of the selected period."""
    one_year_return=pd.DataFrame()
    lookback=min(len(df),252)
    base_price=df["Close"].iloc[-lookback]
    one_year_return["1Y_return"]=(df["Close"]-base_price)/base_price
    return(one_year_return)
def calculate_moving_averages(df):
    """Calculate 20, 50, and 200-day SMA and EMA values."""
    moving_averages=pd.DataFrame()
    moving_averages["SMA_20"]=df["Close"].rolling(20).mean()
    moving_averages["SMA_50"]=df["Close"].rolling(50).mean()
    moving_averages["SMA_200"]=df["Close"].rolling(200).mean()
    moving_averages["EMA_20"]=df["Close"].ewm(span=20,adjust=False).mean()
    moving_averages["EMA_50"]=df["Close"].ewm(span=50,adjust=False).mean()
    moving_averages["EMA_200"]=df["Close"].ewm(span=200,adjust=False).mean()
    return(moving_averages)
def calc_momentum(df):
    """Calculate 5, 20, 30, and 90-day price momentum."""
    momentum=pd.DataFrame()
    momentum["5D"]=df["Close"].pct_change(5)
    momentum["20D"]=df["Close"].pct_change(20)
    momentum["30D"]=df["Close"].pct_change(30)
    momentum["90D"]=df["Close"].pct_change(90)
    return(momentum)
def calc_rsi(df):
    """Calculate 14-period RSI using Wilder's smoothing."""
    rsi=pd.DataFrame()
    rsi["Close"]=df["Close"]
    rsi["change"]=rsi["Close"].diff()
    rsi["gain"]=np.where(rsi["change"]>0,rsi["change"],0)
    rsi["loss"]=np.where(rsi['change']<0,-rsi['change'],0)
    rsi.loc[rsi.index[0],["gain","loss"]]=np.nan#so np.where doesnt make a 0 entry at 0th row in gain and loss instead replaced with nan
    rsi['14d_gainmean']=rsi["gain"].rolling(14).mean()
    rsi['14d_lossmean']=rsi["loss"].rolling(14).mean()
    rsi["wilder_averagegain"]=np.nan
    rsi["wilder_averageloss"]=np.nan
    first_valid = rsi["14d_gainmean"].first_valid_index()
    #creating columns for seeding first valid sma and calculation ewm
    rsi["temp_gain"]=rsi["gain"].copy()
    rsi["temp_loss"]=rsi["loss"].copy()
    #seeding first valid sma
    rsi.loc[first_valid,"temp_gain"]=rsi.loc[first_valid,"14d_gainmean"]
    rsi.loc[first_valid,"temp_loss"]=rsi.loc[first_valid,"14d_lossmean"]
    #calculating ewm for rows[first_valid_position:] and putting them inside wilder average gain and wilder average loss
    rsi.loc[first_valid:,"wilder_averagegain"]=rsi.loc[first_valid:,"temp_gain"].ewm(alpha=1/14,adjust=False).mean()
    rsi.loc[first_valid:,"wilder_averageloss"]=rsi.loc[first_valid:,"temp_loss"].ewm(alpha=1/14,adjust=False).mean()
    rsi["RS"]=rsi["wilder_averagegain"]/rsi["wilder_averageloss"]
    rsi["RSI"]=(100-100/(1+rsi["RS"]))
    return(rsi[["RSI"]])##only returning RSI column as a dataframe
def volume_metrics(df):
    """Calculate volume changes, 20-day average volume, RVOL, and OBV."""
    volume_metrics=pd.DataFrame()
    volume_metrics["volume"]=df["Volume"].copy()
    volume_metrics["daily_vol_change"]=volume_metrics["volume"].diff()
    volume_metrics["daily_%_change"]=volume_metrics["volume"].pct_change()
    volume_metrics["avg_volume_20d"]=volume_metrics["volume"].rolling(20).mean()
    volume_metrics["RVOL"]=volume_metrics["volume"]/volume_metrics["avg_volume_20d"]
    volume_metrics["OBV"]=np.nan
    volume_metrics["daily_price_change"]=df["Close"].diff()
    volume_metrics["signed_volume"]=np.nan
    #calculating signed volume using np.select for multiple conditions
    volume_metrics["signed_volume"]=np.select(
    [volume_metrics["daily_price_change"]>0,
     volume_metrics["daily_price_change"]<0,
     volume_metrics["daily_price_change"]==0,
     volume_metrics["daily_price_change"].isna()],
    [
        volume_metrics["volume"],-volume_metrics["volume"],0,volume_metrics["volume"]
    ],
    default=np.nan
    )
    volume_metrics["OBV"]=volume_metrics["signed_volume"].cumsum()
    return(volume_metrics[["volume","daily_vol_change","daily_%_change","avg_volume_20d","RVOL","OBV"]])
#moving average convergence divergence to indicate whether the momentum is bullish or bearish
def calculate_macd(df):
    """Calculate the 12/26/9 MACD, signal line, and histogram."""
    macd_dataframe=pd.DataFrame()
    macd_dataframe["EMA12"]=df["Close"].ewm(span=12,adjust=False).mean()
    macd_dataframe["EMA26"]=df["Close"].ewm(span=26,adjust=False).mean()
    macd_dataframe["MACD"]=macd_dataframe["EMA12"]-macd_dataframe["EMA26"]
    macd_dataframe["MACD_SIGNAL"]=macd_dataframe["MACD"].ewm(span=9,adjust=False).mean()
    macd_dataframe["MACD_HISTOGRAM"]=macd_dataframe["MACD"]-macd_dataframe["MACD_SIGNAL"]
    return(macd_dataframe[["MACD","MACD_SIGNAL","MACD_HISTOGRAM"]])
#bb is a volatility indicator
def calculate_bollinger_bands(df):
    """Calculate 20-day Bollinger Bands using 2 standard deviations."""
    bollinger_bands=pd.DataFrame()
    bollinger_bands["MIDDLE_BAND"]=df["Close"].rolling(20).mean()
    bollinger_bands["std_20"]=df["Close"].rolling(20).std(ddof=0)#ddof=0:the group provided is the entire thing of interest,ddof=1 the group provided is part of a larger data
    bollinger_bands["UPPER_BAND"]=bollinger_bands["MIDDLE_BAND"]+2*bollinger_bands["std_20"]
    bollinger_bands["LOWER_BAND"]=bollinger_bands["MIDDLE_BAND"]-2*bollinger_bands["std_20"]
    return(bollinger_bands[["MIDDLE_BAND","UPPER_BAND","LOWER_BAND"]])
def calculate_atr(df):
    """Calculate 14-period Average True Range using Wilder's smoothing."""
    atr=pd.DataFrame()
    atr["high-low"]=df["High"]-df["Low"]
    atr["abs_high-prevclose"]=(df["High"]-df["Close"].shift(1)).abs()
    atr["abd_low-prevclose"]=(df["Low"]-df["Close"].shift(1)).abs()
    atr["tr"]=atr.max(axis=1)
    atr["atr"]=np.nan
    initial_atr=atr["tr"].iloc[:14].mean()
    #wilder atr
    atr.iloc[13:,atr.columns.get_loc("atr")]=(pd.concat([pd.Series([initial_atr]),atr["tr"].iloc[14:]]).ewm(alpha=1/14,adjust=False).mean().values)
    return(atr[["atr"]])
def calc_52w_metrics(df):
    """Calculate 52-week high, low, and percentage distances from each."""
    metrics_52w=pd.DataFrame()
    #approx 252 trading days in 52 weeks
    metrics_52w["52_week_high"] = df["High"].rolling(252).max()
    metrics_52w["52_week_low"] = df["Low"].rolling(252).min()
    metrics_52w["distance_from_high"] = ((df["Close"] - metrics_52w["52_week_high"])/ metrics_52w["52_week_high"]) * 100
    metrics_52w["distance_from_low"] = ((df["Close"] - metrics_52w["52_week_low"])/ metrics_52w["52_week_low"]) * 100
    return(metrics_52w)
def calculate_all(df):
    price_metrics=calculate_price_metrics(df)
    one_year_return=calc_1y_return(df)
    moving_averages=calculate_moving_averages(df)
    rsi=calc_rsi(df)
    atr=calculate_atr(df)
    macd=calculate_macd(df)
    volume=volume_metrics(df)
    calculated_df=pd.concat([df["Close"],price_metrics["daily_return"]*100,price_metrics["cumulative_return"]*100,one_year_return["1Y_return"]*100,moving_averages,rsi,atr,macd,volume["OBV"]],axis=1)
    return(calculated_df)