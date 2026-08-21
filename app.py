import streamlit as st
from src.name_to_Ticker import name_to_ticker
from src.data_cleaning import data_clean
from src.data_import import load_stock_data
from src.calculations import calculate_all
from src.plots import price_sma_ema_volume_bb,plot_rsi,plot_macd,plot_atr,plot_obv
st.set_page_config(
    layout="wide"
)
st.title("Technical Stock Screener",text_alignment="center")
mode=st.segmented_control(
    "Choose a mode",
    ["Individual Stock Analysis", "Stock Screener"]
)
if mode == "Individual Stock Analysis":
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
        period = st.radio("Select Period for data",["6mo","1y","2y","5y","10y","max"])          
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
            st.metric("RSI 14",f"{latest["RSI"]:.2f}")
            col1,col2,col3=st.columns(3)

            with col1:
                st.metric("MACD",f"{latest["MACD"]:.2f}")
            with col2:
                st.metric("MACD Signal",f"{latest["MACD_SIGNAL"]:.2f}")
            with col3:
                st.metric("MACD Histogram",f"{latest["MACD_HISTOGRAM"]:.2f}")
            fig_rsi=plot_rsi(df)
            st.plotly_chart(fig_rsi)
            fig_macd=plot_macd(df)
            st.plotly_chart(fig_macd)
            #plotting volatility indicators
            st.subheader("Volatility")
            st.metric("ATR 14",f"{latest["atr"]:.2f}")
            fig_atr=plot_atr(df)
            st.plotly_chart(fig_atr)
            st.subheader("Volume")
            fig_obv=plot_obv(df)
            st.plotly_chart(fig_obv)