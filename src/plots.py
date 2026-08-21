import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from . import calculations
import yfinance as yf
"""
plots for price,smaema,bollinger band
plot for rsi
plot for atr
plot for macd
plot for obv
"""
#REMOVE NON TRADING DAYS FUNCTION,helper function
def remove_non_trading_days(fig, df):

    all_days = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )

    missing_days = all_days.difference(df.index)

    missing_weekdays = missing_days[missing_days.weekday < 5]

    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]),
            dict(values=missing_weekdays)
        ]
    )

    return fig



def price_sma_ema_volume_bb(df):
    fig=make_subplots(shared_xaxes=True,rows=2,cols=1,row_heights=[0.85, 0.15],vertical_spacing=0)
    fig.add_trace(go.Candlestick(x=df.index,open=df["Open"],high=df["High"],low=df["Low"],close=df["Close"],name="PRICE"),row=1,col=1)
    ma=calculations.calculate_moving_averages(df)
    bb=calculations.calculate_bollinger_bands(df)
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
    #BOLLINGER BANDS
    fig.add_trace(go.Scatter(x=bb.index,y=bb["UPPER_BAND"],name="BB UPPER",mode="lines"),row=1,col=1)
    fig.add_trace(go.Scatter(x=bb.index,y=bb["MIDDLE_BAND"],name="BB MIDDLE",mode="lines"),row=1,col=1)
    fig.add_trace(go.Scatter(x=bb.index,y=bb["LOWER_BAND"],name="BB LOWER",mode="lines"),row=1,col=1)
    
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
        height=1000,
        xaxis_rangeslider_visible=False
    )
    fig=remove_non_trading_days(fig,df)

    return(fig)

# #testing
# df=yf.Ticker("AAPL").history(period="1y")
# figure=price_sma_ema_volume_bb(df)
# figure.show()

def plot_rsi(df):
    
    rsi=calculations.calc_rsi(df)
    fig_rsi=go.Figure()
    fig_rsi.add_trace(
        go.Scatter(
            x=rsi.index,
            y=rsi["RSI"],
            mode="lines",
            name="RSI"
        )
    )
    #overbought
    fig_rsi.add_hline(
        y=70,
        line_dash="dash",
        line_color="red",
        annotation_text="overbought(70)"
    )
    #oversold
    fig_rsi.add_hline(
        y=30,
        line_dash="dash",
        line_color="green",
        annotation_text="oversold(30)"
    )
    #midline
    fig_rsi.add_hline(
        y=50,
        line_dash="dot",
        annotation_text="50"
    )
    fig_rsi.update_layout(
        height=400,
        title="RSI 14",
        xaxis_title="Date",
        yaxis=dict(range=[0,100],title="RSI"),
        
    )
    fig_rsi=remove_non_trading_days(fig_rsi,df)
    return(fig_rsi)
#testing
# df=yf.Ticker("AAPL").history(period="2y")
# f=plot_rsi(df)
# f.show()


def plot_atr(df):
    atr=calculations.calculate_atr(df)
    fig_atr=go.Figure()
    fig_atr.add_trace(
        go.Scatter(
            x=atr.index,
            y=atr["atr"],
            mode="lines",
            name="ATR"
        )
    )
    fig_atr.update_layout(
        title="ATR 14",
        xaxis_title="Date",
        yaxis_title="ATR",
        height=400
    )
    return(fig_atr)
#testing
# f=plot_atr(df)
# f.show()

def plot_macd(df):
    macd = calculations.calculate_macd(df)

    fig_macd = go.Figure()

    # MACD line
    fig_macd.add_trace(
        go.Scatter(
            x=macd.index,
            y=macd["MACD"],
            mode="lines",
            name="MACD"
        )
    )

    # Signal line
    fig_macd.add_trace(
        go.Scatter(
            x=macd.index,
            y=macd["MACD_SIGNAL"],
            mode="lines",
            name="Signal"
        )
    )

    # Histogram
    fig_macd.add_trace(
        go.Bar(
            x=macd.index,
            y=macd["MACD_HISTOGRAM"],
            name="Histogram"
        )
    )
    fig_macd.update_layout(
        height=400,
        bargap=0
    )
    fig_macd=remove_non_trading_days(fig_macd,df)
    return(fig_macd)
#testing
# df=yf.Ticker("AAPL").history(period="1y")
# macd=plot_macd(df)
# macd.show()
def plot_obv(df):

    obv=calculations.volume_metrics(df)

    fig_obv = go.Figure()

    fig_obv.add_trace(
        go.Scatter(
            x=obv.index,
            y=obv["OBV"],
            mode="lines",
            name="OBV"
        )
    )

    fig_obv.update_layout(
        title="OBV",
        xaxis_title="Date",
        yaxis=dict(title="OBV"),
        height=400
    )

    fig_obv = remove_non_trading_days(fig_obv, df)

    return fig_obv
#testing
# df=yf.Ticker("AAPL").history(period="1y")
# obv=plot_obv(df)
# obv.show()