import yfinance as yf
def load_stock_data(symbol,period="1y",interval="1d"):
    """
    IMPORTS DATA FROM YFINANCE GIVEN THE TICKER OR NAME OF THE COMPANY for 1 year
    parameters:
    symbol=stock ticker(str)
    period=time period to download for
    interval=candle interval
    
    returns:
    pandas.df
    
    """
    data=yf.Ticker(symbol)
    df=data.history(period=period)
    return(df)
    