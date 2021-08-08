from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic import TemplateView
from . import views as order_views

from django.conf import settings

app_name='order'
urlpatterns = [
    path('list', order_views.OrderListPageView.as_view(), name='show_orderList'),
]
