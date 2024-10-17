import pandas as pd
from .models import StockPrice

def backtest(initial_investment, symbol):
    # Fetch data from the database
    data = StockPrice.objects.filter(symbol=symbol).order_by('date').values()
    df = pd.DataFrame(data)
    
    # Calculate moving averages
    df['50_ma'] = df['close_price'].rolling(window=50).mean()
    df['200_ma'] = df['close_price'].rolling(window=200).mean()

    # Define backtesting logic
    in_position = False
    balance = initial_investment
    quantity = 0

    for _, row in df.iterrows():
        if not in_position and row['close_price'] < row['50_ma']:
            # Buy signal
            in_position = True
            quantity = balance / row['close_price']
        elif in_position and row['close_price'] > row['200_ma']:
            # Sell signal
            in_position = False
            balance = quantity * row['close_price']
            quantity = 0

    return {
        'final_balance': balance,
        'return_percent': (balance - initial_investment) / initial_investment * 100
    }
