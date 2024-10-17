import requests
from django.core.management.base import BaseCommand
from financial_data.models import StockPrice
import datetime

class Command(BaseCommand):
    help = 'Fetch daily stock prices for a specific symbol from Alpha Vantage'

    def handle(self, *args, **kwargs):
        API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'  # Replace with your actual API key
        symbol = 'AAPL'
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'

        response = requests.get(url)
        data = response.json()

        if 'Time Series (Daily)' in data:
            time_series = data['Time Series (Daily)']
            for date_str, daily_data in time_series.items():
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                StockPrice.objects.update_or_create(
                    symbol=symbol,
                    date=date,
                    defaults={
                        'open_price': float(daily_data['1. open']),
                        'high_price': float(daily_data['2. high']),
                        'low_price': float(daily_data['3. low']),
                        'close_price': float(daily_data['4. close']),
                        'volume': int(daily_data['5. volume']),
                    }
                )
            self.stdout.write(self.style.SUCCESS('Successfully fetched and stored stock prices'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from Alpha Vantage'))
