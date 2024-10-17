from django.urls import path
from . import views

urlpatterns = [
    path('stock_prices/', views.stock_price_list, name='stock_price_list'),
    path('run_backtest/', views.run_backtest, name='run_backtest'),
    path('predict_stock_price/', views.predict_stock_price, name='predict_stock_price'),
    path('generate_report/', views.generate_report, name='generate_report'),
]
