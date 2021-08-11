from django.shortcuts import render, redirect
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json

from .models import CustomerModel
from .forms import CustomerAddForm 

# Create your views here.

##BEGIN: Add by SRJ-SGL 
#客户列表
class CustomerListPageView(LoginRequiredMixin, ListView):
    ## login_url = "/account/login/"  和下边一行的功能是一样的,一个是硬编码,一个是灵活实现
    login_url = reverse_lazy('user_login') 
    template_name = "customer/customer-list.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        ## 过滤条件参数
        ## 判断是搜索的数据还是直接显示的数据
        q = {}
        page = request.POST.get('page')
        rows = request.POST.get('limit')

        filter_customer = request.POST.get('filter_customer')         
        filter_contact = request.POST.get('filter_contact')         
        filter_phone = request.POST.get('filter_phone')         

        if filter_customer:
            q['customer'] = filter_customer
        if filter_contact:
            q['contact'] = filter_contact
        if filter_phone:
            q['phone'] = filter_phone

        customers = CustomerModel.objects.filter(**q)

        start = (int(page) - 1) * int(rows)
        end = (int(page) - 1) * int(rows) + int(rows)

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
        resultdict = {}

        if formObj.is_valid():
            form_cd = formObj.cleaned_data 
            new_otrequest = formObj.save(commit=False)
            new_otrequest.save(form_cd)

            resultdict['code'] = 0
            resultdict['msg'] = ""
            return JsonResponse(resultdict, safe=False) 
            ##return redirect("customer:show_customerList")

        return self.render_to_response({"form":formObj})

class CustomerDelPageView(LoginRequiredMixin, DeleteView):
    login_url = "/account/login/"
    success_url = reverse_lazy('customer:show_customerList')

    model = CustomerModel

    def delete(self, request, *args, **kwargs):
        ##for k, v in kwargs.items():
        ##    print ('%s，%s；' , (k, v))
        super(CustomerDelPageView, self).delete(request, *args, **kwargs)
        return JsonResponse({'code':0, 'msg':''}) 

class CustomerDetailPageView(LoginRequiredMixin, DeleteView):
    template_name = "customer/customer-update.html"
    context_object_name = "customer"

    model = CustomerModel

    ##如果不要下边的这个函数,是不会把信息返回到表单的
    ##def get_object(self, queryset=None):
    ##    obj = super(CustomerDetailPageView, self).get_object()
    ##    return obj

    ##下边注释的两个函数其实放开效果是一样的,只不过是记录一下怎么取url中的参数的方法
    ##def get_object(self,queryset=None):
    ##    obj_id = int(self.kwargs.get(self.pk_url_kwarg, None))
    ##    obj = self.model.objects.get(id = obj_id)
    ##    return obj 
    
    def get_context_data(self, **kwargs):
        context = super(CustomerDetailPageView, self).get_context_data(**kwargs)
        return context

class CustomerUpdatePageView(LoginRequiredMixin, UpdateView):
    login_url = "/account/login/"
    success_url = reverse_lazy('customer:show_customerList')

    template_name = "customer/customer-update.html"
    template_name_suffix = '_update_form'
    fields = ['customer', 'contact', 'phone']
    context_object_name = "customer"

    model = CustomerModel

    ##以下的方式也可以用,相当于自己实现更新这个功能
    ##form_class = CustomerAddForm 

    ##def get_context_data(self, **kwargs):
    ##    context = super(CustomerUpdatePageView,self).get_context_data(**kwargs)
    ##    return context

    ##def post(self, request, *args, **kwargs):
    ##    formObj = CustomerAddForm(request.POST)
    ##    resultdict = {}

    ##    if formObj.is_valid():
    ##        form_cd = formObj.cleaned_data 

    ##        original = super(CustomerUpdatePageView, self).get_object()
    ##        ##original.customer = form_cd['customer']
    ##        ##original.contact= form_cd['contact']
    ##        ##original.phone= form_cd['phone']
    ##        original.save(form_cd)

    ##        resultdict['code'] = 0
    ##        resultdict['msg'] = ""
    ##        return JsonResponse(resultdict, safe=False) 

    ##    resultdict['code'] = 1
    ##    resultdict['msg'] = "update failed."
    ##    return JsonResponse(resultdict, safe=False) 

##END: Add by SRJ-SGL 
