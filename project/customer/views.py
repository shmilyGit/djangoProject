from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.

##BEGIN: Add by SRJ-SGL 
#客户列表
class CustomerListPageView(LoginRequiredMixin, TemplateView):
    template_name = "customer/customer-list.html"

class CustomerAddPageView(LoginRequiredMixin, TemplateView):
    template_name = "customer/customer-add.html"

##END: Add by SRJ-SGL 
