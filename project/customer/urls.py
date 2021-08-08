from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic import TemplateView
from . import views as customer_views

from django.conf import settings

app_name='customer'
urlpatterns = [
    path('list', customer_views.CustomerListPageView.as_view(), name='show_customerList'),
    path('add', customer_views.CustomerAddPageView.as_view(), name='show_customerAdd'),
]
