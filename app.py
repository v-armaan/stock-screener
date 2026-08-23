import streamlit as st
from src.name_to_Ticker import name_to_ticker
from src.data_cleaning import data_clean
from src.data_import import load_stock_data,get_sp500,get_nifty50,get_sensex
from src.calculations import calculate_all
from src.plots import price_sma_ema_volume_bb,plot_rsi,plot_macd,plot_atr,plot_obv
from src.screening import  screen_stock,screen_stocks
import pandas as pd
st.set_page_config(
    layout="wide"
)
METRICS=[
                "Close",
                "Daily Return",
                "Cumulative Return",
                "SMA_20",
                "SMA_50",
                "SMA_200",
                "EMA_20",
                "EMA_50",
                "EMA_200",
                "RSI",
                "MACD",
                "MACD_SIGNAL",
                "MACD_HISTOGRAM",
                "ATR",
                "OBV"
            ]
st.title("Technical Stock Screener",text_alignment="center")
mode=st.segmented_control(
    "Choose a mode",
    ["Individual Stock Analysis", "Stock Screener"],key="mode"
)
#INDIVIDUAL ANALYSIS MODE
if mode == "Individual Stock Analysis":
        if "selected_ticker" in st.session_state:
            selected_ticker=st.session_state.selected_ticker
            st.write("Selected Ticker:",selected_ticker)
            if st.button("Search a different stock"):
                del st.session_state.selected_ticker
                st.rerun()
        else:
            st.subheader("Search for a stock")
            search_query = st.text_input("Enter company name or ticker")
            if st.button("Search"):
                st.session_state.results = name_to_ticker(search_query)
            if "results" in st.session_state:
                results = st.session_state.results
                options = []
                for i in results:
                    company_name = i["shortname"]
                    ticker = i["symbol"]
                    option = f"{company_name} ({ticker})"
                    options.append(option)
                selected_stock = st.selectbox("Select a stock", options)
                for i in results:
                    company_name = i["shortname"]
                    ticker = i["symbol"]
                    option = f"{company_name} ({ticker})"
                    if option == selected_stock:
                        selected_ticker = ticker
                        break
                st.write("selected ticker:", selected_ticker)
        period = st.radio("Select Period for data",["6mo","1y","2y","5y","10y","max"],index=1)          
        analyze_stock=st.button("Analyze Stock")
        if analyze_stock:
            
            df=load_stock_data(selected_ticker,period)
            df=data_clean(df)
            calculated_df=calculate_all(df)
            latest=calculated_df.iloc[-1]
            st.subheader("Price")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Close", f"{latest['Close']:.2f}")#only give 2 decimal places
            with col2:
                st.metric("Daily Return", f"{latest['daily_return']:.2%}")#convert return to 2 decimal places and percentage
            with col3:
                st.metric("Cumulative Return", f"{latest['cumulative_return']:.2%}")
            st.subheader("Moving Averages")
            col1,col2,col3=st.columns(3)
            with col1:
                st.metric("SMA 20",f"{latest['SMA_20']:.2f}")
            with col2:
                st.metric("SMA 50",f"{latest['SMA_50']:.2f}")
            with col3:
                st.metric("SMA 200",f"{latest['SMA_200']:.2f}")
            with col1:
                st.metric("EMA 20",f"{latest['EMA_20']:.2f}")
            with col2:
                st.metric("EMA 50",f"{latest['EMA_50']:.2f}")
            with col3:
                st.metric("EMA 200",f"{latest['EMA_200']:.2f}")
            fig=price_sma_ema_volume_bb(df)
            st.plotly_chart(fig,use_container_width=True)
            st.subheader("Momentum")
            st.metric("RSI 14",f"{latest['RSI']:.2f}")
            col1,col2,col3=st.columns(3)

            with col1:
                st.metric("MACD",f"{latest['MACD']:.2f}")
            with col2:
                st.metric("MACD Signal",f"{latest['MACD_SIGNAL']:.2f}")
            with col3:
                st.metric("MACD Histogram",f"{latest['MACD_HISTOGRAM']:.2f}")
            fig_rsi=plot_rsi(df)
            st.plotly_chart(fig_rsi)
            fig_macd=plot_macd(df)
            st.plotly_chart(fig_macd)
            #plotting volatility indicators
            st.subheader("Volatility")
            st.metric("ATR 14",f"{latest['atr']:.2f}")
            fig_atr=plot_atr(df)
            st.plotly_chart(fig_atr)
            st.subheader("Volume")
            fig_obv=plot_obv(df)
            st.plotly_chart(fig_obv)
#SCREENING MODE
elif mode == "Stock Screener":

    screen_choice = st.radio(
        "CHOOSE AN INDEX OR CREATE CUSTOM LIST:",
        ["S&P500", "NIFTY50", "SENSEX", "CUSTOM LIST"]
    )

    custom_tickers_input = ""
    if screen_choice == "CUSTOM LIST":
        custom_tickers_input = st.text_input(
            "Enter tickers separated by commas (e.g. AAPL, MSFT, TSLA)"
        )

    period = st.radio(
        "Select Period for data",
        ["6mo", "1y", "2y", "5y", "10y", "max"]
    )

    st.write(f"SCREENING {screen_choice} stocks")
    
    # initializing condition counter
    if "condition_counter" not in st.session_state:
        st.session_state.condition_counter = 1

    # initializing conditions
    if "conditions" not in st.session_state:
        st.session_state.conditions = []

    # make sure there is one saved condition for every condition widget
    while len(st.session_state.conditions) < st.session_state.condition_counter:
        st.session_state.conditions.append(
            ("Close", "<", 0.0)
        )

    conditions = []

    for i in range(st.session_state.condition_counter):

        st.write(f"Condition {i+1}")

        current_metric = st.session_state.conditions[i][0]
        current_operator = st.session_state.conditions[i][1]
        current_value = st.session_state.conditions[i][2]

        col1, col2, col3 = st.columns(3)

        with col1:
            metric = st.selectbox(
                "Metric",
                METRICS,
                index=METRICS.index(current_metric),
                key=f"metric_widget{i}"
            )

        with col2:
            operator = st.selectbox(
                "Operator",
                ["<", "<=", ">", ">=", "=="],
                index=["<", "<=", ">", ">=", "=="].index(current_operator),
                key=f"operator_widget{i}"
            )

        with col3:
            value = st.number_input(
                "Value",
                value=float(current_value),
                key=f"value_widget{i}"
            )

        # save current values permanently
        st.session_state.conditions[i] = (
            metric,
            operator,
            value
        )

        conditions.append(
            (metric, operator, value)
        )
            
        #add condtion button
    def add_condition():
        st.session_state.condition_counter+=1
    st.button("Add Condition",on_click=add_condition)

        # SCREENING
    if st.button("Screen Stocks"):
        tickers = []
        if screen_choice == "S&P500":
            tickers = get_sp500()
        elif screen_choice == "NIFTY50":
            tickers = get_nifty50()
        elif screen_choice == "SENSEX":
            tickers = get_sensex()
        elif screen_choice == "CUSTOM LIST":
            tickers = [
                t.strip().upper()
                for t in custom_tickers_input.split(",")
                if t.strip() != ""
            ]

        if len(tickers) == 0:
            st.warning("No tickers to screen. Please provide at least one ticker.")
        else:
            with st.spinner(f"Downloading and Screening {screen_choice} stocks..."):
                st.session_state.stored_df = screen_stocks(
                    tickers,
                    conditions,
                    period
                )

    # DISPLAY RESULTS - outside the "Screen Stocks" button block so it
    # survives reruns triggered by the checkbox / selectbox / More Info button
    if "stored_df" in st.session_state:
        display_df = pd.DataFrame()
        show_all = st.checkbox("Show all metrics")
        if show_all:
            for ticker in st.session_state.stored_df:
                latest = st.session_state.stored_df[ticker]["calculated"].iloc[-1]
                latest["Ticker"] = ticker
                display_df = pd.concat(
                    [display_df, latest.to_frame().T],
                    ignore_index=True
                )
        else:
            metrics = []
            for condition in conditions:
                if condition[0] not in metrics:
                    metrics.append(condition[0])
            for ticker in st.session_state.stored_df:
                latest = st.session_state.stored_df[ticker]["calculated"].iloc[-1]
                latest = latest[metrics]
                latest["Ticker"] = ticker
                display_df = pd.concat(
                    [display_df, latest.to_frame().T],
                    ignore_index=True
                )
        display_df.insert(0, "Ticker", display_df.pop("Ticker"))
        st.dataframe(
            display_df,
            height="content"
        )
        #switching modes
        st.subheader("For detailed analysis of a stock in the screened list select its ticker and click on more info")
        chosen_ticker = st.selectbox("Select stock",list(st.session_state.stored_df.keys()),width=150)
        def switch_to_individual():
            st.session_state.selected_ticker = chosen_ticker
            st.session_state.mode="Individual Stock Analysis"
            return()
        st.button("More Info",on_click=switch_to_individual)