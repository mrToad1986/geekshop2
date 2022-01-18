"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from mainapp.views import index
from mainapp.views import contact

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('contact/', contact, name='contact'),
    path('basket', include('basketapp.urls', namespace='basketapp')),
    path('orders', include('ordersapp.urls', namespace='ordersapp')),
    path('', include('social_django.urls', namespace='social')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
