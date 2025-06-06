import pandas as pd
import numpy as np
import talib
# import ta as talib
import matplotlib.pyplot as plt

def analyze_stock_data(file_path):
    # Load stock price data
    df = pd.read_csv(file_path)

    # Ensure data includes required columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']] #this is to make sure that the columns are in the correct order
    df['Date'] = pd.to_datetime(df['Date']) #this is to make sure that the date column is in the correct format
    df.set_index('Date', inplace=True)


    # Apply TA-Lib indicators
    df['SMA'] = talib.SMA(df['Close'], timeperiod=20)  # Simple Moving Average
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)  # Relative Strength Index
    df['MACD'], df['MACDSignal'], df['MACDHist'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)  # MACD

    # Calculate daily returns
    df['Return'] = df['Close'].pct_change()

    # Calculate annual volatility
    annual_volatility = df['Return'].std() * np.sqrt(252)  # Assuming 252 trading days in a year
    print(f"Annual Volatility: {annual_volatility}")

    # Visualize data
    plt.figure(figsize=(14, 7))

    # Plot Close price and SMA
    plt.subplot(2, 1, 1) # 2 rows, 1 column, first subplot
    plt.plot(df['Close'], label='Close Price')
    plt.plot(df['SMA'], label='20-Day SMA', color='orange')
    plt.title('Close Price and 20-Day SMA')
    plt.legend()

    # Plot RSI
    plt.subplot(2, 1, 2) # 2 rows, 1 column, second subplot
    plt.plot(df['RSI'], label='RSI', color='red')
    plt.axhline(70, linestyle='--', color='gray') # Overbought threshold
    plt.axhline(30, linestyle='--', color='gray') # Oversold threshold
    plt.title('Relative Strength Index (RSI)')
    plt.legend()

    plt.tight_layout()
    plt.show()

