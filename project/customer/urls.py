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
    path('<int:pk>/delete', customer_views.CustomerDelPageView.as_view(), name='show_customerDel'),
    path('<int:pk>/detail', customer_views.CustomerDetailPageView.as_view(), name='show_customerDetail'),
    path('<int:pk>/update', customer_views.CustomerUpdatePageView.as_view(), name='show_customerUpdate'),

    ##修改记录时有两种方式
    ##一是先用DetailView类获取要修改的对象将对象的数据回显到修改表单中,再使用UpdateView类去更新对象
    ##二是直接使用UpdateView类对象,在XXX_UpdateView类中添加一个获取对象的函数即可(get_context_data)
]
