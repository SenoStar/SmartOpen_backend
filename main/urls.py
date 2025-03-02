from . import views
from django.urls import path

from .views import login_view, register_view, logout_view, catalog, korzina, cooperation, purchase_product

app_name = 'pages'

urlpatterns = [
    path('', views.main, name='about'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('catalog/', catalog, name='catalog'),
    path('korzina/', korzina, name='korzina'),
    path('cooperation/', cooperation, name='cooperation'),
    path('purchase/<int:product_id>/', purchase_product, name='purchase_product'),
]