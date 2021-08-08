from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.

##BEGIN: Add by SRJ-SGL 
#订单列表
class OrderListPageView(LoginRequiredMixin, TemplateView):
    template_name = "order/order-list.html"
##END: Add by SRJ-SGL 
