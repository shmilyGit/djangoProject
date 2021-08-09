from django.shortcuts import render, redirect
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import CustomerModel
from .forms import CustomerAddForm 

# Create your views here.

##BEGIN: Add by SRJ-SGL 
#客户列表
class CustomerListPageView(LoginRequiredMixin, TemplateView):
    login_url = "/account/login/"
    template_name = "customer/customer-list.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        page = request.POST.get('page')
        rows = request.POST.get('limit')

        start = (int(page) - 1) * int(rows)
        end = (int(page) - 1) * int(rows) + int(rows)

        customers  = CustomerModel.objects.all()
        total = customers.count()

        customers = customers[start:end]

        dict = []
        resultdict = {}

        for tmp in customers:
            dic = {}
            dic['id'] = tmp.id
            dic['customer'] = tmp.customer
            dic['contact'] = tmp.contact
            dic['phone'] = tmp.phone
            dic['created'] = tmp.created.strftime("%Y-%m-%d %H:%M:%S")
            dict.append(dic)

        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['count'] = total 
        resultdict['data'] = dict

        return JsonResponse(resultdict, safe=False) 

class CustomerAddPageView(LoginRequiredMixin, CreateView):
    login_url = "/account/login/"
    template_name = "customer/customer-add.html"
    fields = ['customer', 'contact', 'phone']

    ##Note1 当继承的是TemplateView时使用这个
    ##def get(self, request):
    ##    return render(request, "customer/customer-add.html")
    
    ##Note2 当继承的是CreateView时使用这个,功能与Note1是一样的,只是两种不同的实现方式
    queryset = CustomerModel.objects.all()

    def post(self, request, *args, **kwargs):
        formObj = CustomerAddForm(request.POST)

        if formObj.is_valid():
            form_cd = formObj.cleaned_data 
            new_otrequest = formObj.save(commit=False)
            new_otrequest.save(form_cd)
            return redirect("customer:show_customerList")

        return self.render_to_response({"form":formObj})

##END: Add by SRJ-SGL 
