import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calculations
import yfinance as yf
def price_sma_ema_volume(df):
    fig=make_subplots(shared_xaxes=True,rows=2,cols=1)
    fig.add_trace(go.Candlestick(x=df.index,open=df["Open"],high=df["High"],low=df["Low"],close=df["Close"],name="PRICE"),row=1,col=1)
    ma=calculations.calculate_moving_averages(df)
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ma["SMA_20"],
            name="SMA 20"
        ),
        row=1,
        col=1
    )
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=ma["EMA_20"],
            name="EMA 20"
            ),
        row=1,
        col=1
    )
    volume_color=[]
    #assigning color to volume bars according to candlestick colors
    for i in range(len(df)):
        if df["Close"].iloc[i]>df["Open"].iloc[i]:
            volume_color.append("green")
        else:
            volume_color.append("red")
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color=volume_color,
            name="Volume"
        ),
        row=2,
        col=1
    )
    fig.update_layout(
        height=800,
        xaxis_rangeslider_visible=False,
        plot_bgcolor="black"
    )
    return(fig)

#testing
df=yf.Ticker("AAPL").history(period="1y")
figure=price_sma_ema_volume(df)
figure.show()
