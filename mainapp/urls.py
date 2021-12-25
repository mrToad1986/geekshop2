from django.urls import path, include
from mainapp.views import products

app_name = 'products'

urlpatterns = [
    path('', products, name='products'),
    path('<int:pk>/', products, name='category'),
]
