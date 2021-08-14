from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic import TemplateView
from . import views as order_views

from django.conf import settings

app_name='order'
urlpatterns = [
    path('list', order_views.OrderListPageView.as_view(), name='show_orderList'),
    path('add', order_views.OrderAddPageView.as_view(), name='show_orderAdd'),
    path('<int:pk>/delete', order_views.OrderDelPageView.as_view(), name='show_orderDel'),
    path('<int:pk>/update', order_views.OrderUpdatePageView.as_view(), name='show_orderUpdate'),
    ##path('<int:pk>/detail', order_views.OrderDetailPageView.as_view(), name='show_orderDetail'),
]
