import yfinance as yf
import requests
import pandas as pd
from io import StringIO
import streamlit as st
@st.cache_data(ttl=3600)#cache data for 1 hour
def load_stock_data(symbol,period="1y"):
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

def get_sp500():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)#response is a .txt ie a huge string
    sp500 = pd.read_html(StringIO(response.text))[0]#stringio converts that giant string into a file like object that contains that html that pd can read
    tickers = sp500["Symbol"].tolist()
    tickers = [ticker.replace(".", "-") for ticker in tickers]#yfinance uses - wehreas wiki uses . for special symbols not exchange suffixes
    return(tickers)#returns a list of tickers

def get_nifty50():
    url ="https://en.wikipedia.org/wiki/NIFTY_50"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)#response is a .txt ie a huge string
    nf50 = pd.read_html(StringIO(response.text))[1]#stringio converts that giant string into a file like object that contains that html that pd can read
    tickers = nf50["Symbol"].dropna().tolist()
    tickers = [ticker+".NS" for ticker in tickers]#adds .NS to end of symbol for yfinance
    return(tickers)#returns a list of tickers

def get_sensex():
    url ="https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)#response is a .txt ie a huge string
    sensex= pd.read_html(StringIO(response.text))[0]#stringio converts that giant string into a file like object that contains that html that pd can read
    tickers = sensex["Symbol"].dropna().tolist()
    return(tickers)#returns a list of tickers
    