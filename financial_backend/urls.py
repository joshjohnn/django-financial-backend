from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

# A simple view function to handle the root URL
def home(request):
    return HttpResponse("Welcome to the Financial Backend API. Use /api/ to access available endpoints.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('financial_data.urls')),  # Include URLs from financial_data app
    path('', home),  # Default path for the root URL
]
