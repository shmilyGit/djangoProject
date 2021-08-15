"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url,include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from account import views as auth_views
from common import views as comm_views

urlpatterns = [
    #登录页
    #直接访问IP:port 后边不用加路径, 即http://192.168.5.105:8000就会跳转到login.html
    #方法一,这样不会在html模板中使用{{form.password}}
	#url('', TemplateView.as_view(template_name="account/login.html"), name='show_loginPage'),
    #方法二,这样可以在html模板中使用{{form.password}}
	path('', auth_views.LoginView.as_view(template_name='account/login.html'), name="show_loginPage"),

    #登录之后跳转到该页,该页即首页
    path('index/', comm_views.IndexPageView.as_view(), name='show_index'),
    path('homepage/', comm_views.HomePageView.as_view(), name='show_homePage'),

    #账户相关
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),

    #客户相关
    path('index/customer/', include('customer.urls', namespace='customer')),

    #订单相关
    path('index/order/', include('order.urls', namespace='order')),

    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
