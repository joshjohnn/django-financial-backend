from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import pickle
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

from .models import StockPrice
from .backtesting import backtest

# Load pre-trained model for prediction
model_path = 'simple_model.pkl'
model = None
if os.path.exists(model_path):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)

# View to list stock prices for a specific symbol
def stock_price_list(request):
    symbol = request.GET.get('symbol', 'AAPL')
    stock_prices = StockPrice.objects.filter(symbol=symbol).order_by('-date')
    data = [
        {
            'date': stock.date,
            'open_price': stock.open_price,
            'high_price': stock.high_price,
            'low_price': stock.low_price,
            'close_price': stock.close_price,
            'volume': stock.volume
        }
        for stock in stock_prices
    ]
    return JsonResponse({'stock_prices': data})

# View to run backtesting logic
@csrf_exempt
def run_backtest(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            symbol = body.get('symbol', 'AAPL')
            initial_investment = body.get('initial_investment', 10000)
            result = backtest(initial_investment, symbol)
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# View to predict future stock prices based on pre-trained model
def predict_stock_price(request):
    if model is None:
        return JsonResponse({'error': 'Model file not found. Prediction is unavailable.'}, status=500)

    symbol = request.GET.get('symbol', 'AAPL')
    data = StockPrice.objects.filter(symbol=symbol).order_by('-date')[:5].values()  # Fetch recent 5 records for prediction
    df = pd.DataFrame(list(data))
    if df.empty:
        return JsonResponse({'error': 'No data available for prediction'}, status=400)

    # Using 'close_price' as the feature for prediction
    features = np.array(df['close_price']).reshape(-1, 1)
    predictions = model.predict(features)
    return JsonResponse({'predictions': predictions.tolist()})

# View to generate a report including visualizations
def generate_report(request):
    symbol = request.GET.get('symbol', 'AAPL')
    data = StockPrice.objects.filter(symbol=symbol).order_by('date').values()
    df = pd.DataFrame(data)

    if df.empty:
        return JsonResponse({'error': 'No data available for generating report'}, status=400)

    # Generate plot for stock prices
    dates = pd.to_datetime(df['date'])
    close_prices = df['close_price']

    plt.figure(figsize=(10, 5))
    plt.plot(dates, close_prices, label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{symbol} Stock Price')
    plt.legend()
    plt.savefig(f'{symbol}_chart.png')

    # Generate a PDF report
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Stock Report for {symbol}", ln=True)
    pdf.image(f'{symbol}_chart.png', x=10, y=20, w=190)
    pdf.output(f"{symbol}_report.pdf")

    # Serve the generated PDF
    with open(f'{symbol}_report.pdf', 'rb') as report_file:
        response = HttpResponse(report_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={symbol}_report.pdf'
        return response
