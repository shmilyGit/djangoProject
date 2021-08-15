from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView
from braces.views import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


from customer.models import CustomerModel as Customer
from order.models import OrderModel as Order 
from django.db.models import F ##一个数据库中的两个字段比较需要用到
import json

##BEGIN: Add by SRJ-SGL 
class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = "frame/index.html"
    login_url = "/account/login/"

class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "frame/homepage.html"
    login_url = "/account/login/"

    def get(self, request):
        customerNum = Customer.objects.all().count()   
        orderNum = Order.objects.all().count()

        q = {}

        q['balance__gt'] = 0
        q['balance__lt'] = F('price')
        expired = Order.objects.filter(balance__lte = 0).count()
        normal = Order.objects.filter(**q).count()
        day7expired = Order.objects.filter(balance__lte = F('price')*7).count()
        day3expired = Order.objects.filter(balance__lte = F('price')*3).count()

        normalobj = Order.objects.filter(**q)

        context = {
            'customerNum':customerNum,
            'orderNum':orderNum,
            'expired':expired,
            'normal':normal,
            'day7expired':day7expired,
            'day3expired':day3expired,
        }

        return render(request, self.template_name, context)
