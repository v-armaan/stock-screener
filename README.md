# Technical Stock Screener

A Streamlit web app for analyzing individual stocks and screening entire indices (S&P 500, NIFTY 50, SENSEX, or a custom list) against user-defined technical conditions.

## Features

**Individual Stock Analysis**
- Search any stock by company name or ticker
- View price, moving averages (SMA/EMA), momentum (RSI, MACD), volatility (ATR), and volume (OBV) metrics
- Interactive candlestick chart with Bollinger Bands and moving averages overlaid
- Return metrics shown for both the selected time period and a fixed trailing 12 months, so results are comparable across different period selections

**Stock Screener**
- Screen the entire S&P 500, NIFTY 50, or SENSEX against custom conditions, or supply your own comma-separated ticker list
- Build multiple conditions (e.g. `RSI < 30`, `Close > SMA_200`) combined with AND logic
- Failed/unavailable tickers are skipped automatically so one bad ticker doesn't break a run
- Jump straight from a screened result into full Individual Stock Analysis for that ticker

## Technical Indicators

All indicators are calculated from scratch using pandas/numpy (no `ta-lib` or `pandas-ta`):

- Simple & Exponential Moving Averages (20/50/200-day)
- RSI (14-period, Wilder's smoothing)
- MACD (12/26/9)
- Bollinger Bands (20-day, 2 std dev)
- Average True Range (14-period, Wilder's smoothing)
- On-Balance Volume (OBV)
- Cumulative return (selected period) and trailing 1-year return

## Tech Stack

- **Streamlit** — UI framework
- **yfinance** — historical OHLCV data
- **yahooquery** — company name → ticker search
- **pandas / numpy** — data cleaning and indicator calculations
- **plotly** — interactive charts

## Project Structure

```
stock-screener/
├── app.py                  # Streamlit UI and app logic
├── src/
│   ├── data_import.py      # yfinance data fetching + index constituent scraping
│   ├── data_cleaning.py    # NaN handling, duplicate removal
│   ├── calculations.py     # technical indicator calculations
│   ├── name_to_Ticker.py   # company name search
│   ├── plots.py            # plotly chart generation
│   └── screening.py        # condition matching + multi-stock screening loop
└── requirements.txt
```

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/v-armaan/stock-screener.git
cd stock-screener
```

**2. Create and activate a virtual environment**

macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

You'll know it's active when your terminal prompt shows `(.venv)` at the start.

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

This opens the app in your browser (usually `http://localhost:8501`).

**Note:** every time you open a new terminal session to work on this project, you need to re-activate the virtual environment first (step 2) before running the app — it doesn't stay active across terminal restarts.


## Known Limitations

- Data is sourced via `yfinance`, an unofficial library that scrapes Yahoo Finance — it has no guaranteed uptime or rate limits, and can occasionally fail or be throttled
- Index constituents (S&P 500, NIFTY 50, SENSEX) are scraped from Wikipedia and may occasionally be out of date if the page structure changes
- Screening a full index (500 tickers) can take a few minutes due to sequential fetching and no official Yahoo rate-limit guarantees
- Prices are shown without currency labels — take care when comparing results across indices priced in different currencies (e.g. USD for S&P 500 vs INR for NIFTY 50/SENSEX)
