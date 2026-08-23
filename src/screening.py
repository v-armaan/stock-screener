
import yfinance as yf
from src import calculations,data_import,data_cleaning
def apply_condition(df, metric, operator, value): #to check if one condition passes

    latest = df.iloc[-1]
    if isinstance(value, str):
        value = latest[value]

    if operator == ">":
        return latest[metric] > value

    elif operator == "<":
        return latest[metric] < value

    elif operator == ">=":
        return latest[metric] >= value

    elif operator == "<=":
        return latest[metric] <= value

    elif operator == "==":
        return latest[metric] == value

    elif operator == "!=":
        return latest[metric] != value

    else:
        raise ValueError("Invalid operator")

def screen_stock(df, conditions):   #to check whether all the conditions pass

    for metric, operator, value in conditions:

        if not apply_condition(df, metric, operator, value):
            return False

    return True
def screen_stocks(tickers, conditions,period):#handle multiple tickers and stores the required ones(those that pass the conditions)
    results={}
    for ticker in tickers:
        try:
            df=data_import.load_stock_data(ticker,period)
            df=data_cleaning.data_clean(df)
            calculated_df=calculations.calculate_all(df)
            if screen_stock(calculated_df,conditions):
                results[ticker]={"df":df,"calculated":calculated_df}
        except Exception as e:
            print(f"{ticker}:Error-{e}")
            continue
    return results
# #testing
# tickers = ["AAPL", "MSFT", "NVDA", "AMZN"]
# conditions = [
#     ("RSI", "<", 30),
#     ("Close", ">", "SMA_200"),
#     ("MACD", ">", "MACD_SIGNAL")
# ]
# results=screen_stocks(tickers,conditions)
# print(results.keys())