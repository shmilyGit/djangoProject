from django.shortcuts import render, redirect
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
import json

from customer.models import CustomerModel
from .models import OrderModel
from .forms import OrderAddForm 

# Create your views here.

##BEGIN: Add by SRJ-SGL 
#客户列表
class OrderListPageView(LoginRequiredMixin, ListView):
    ## login_url = "/account/login/"  和下边一行的功能是一样的,一个是硬编码,一个是灵活实现
    login_url = reverse_lazy('user_login') 
    template_name = "order/order-list.html"
    search_fields = ('orderid', 'customer__name', 'contact', 'phone', 'orderdate')

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        ## 过滤条件参数
        ## 判断是搜索的数据还是直接显示的数据
        q = {}
        page = request.POST.get('page')
        rows = request.POST.get('limit')

        filter_orderid = request.POST.get('filter_orderid')         
        filter_customer = request.POST.get('filter_customer')         
        filter_contact = request.POST.get('filter_contact')         
        filter_phone = request.POST.get('filter_phone')         
        filter_orderdate = request.POST.get('filter_orderdate')
        
        if filter_orderid:
            q['orderid__icontains'] = filter_orderid
        if filter_customer: ##外键不能直接过滤,需要指定过滤外键的哪个字段
            q['customer__name__icontains'] = filter_customer
        if filter_contact:
            q['contact__icontains'] = filter_contact
        if filter_phone:
            q['phone__icontains'] = filter_phone
        if filter_orderdate:
            q['orderdate__icontains'] = filter_orderdate

        orders = OrderModel.objects.filter(**q)

        start = (int(page) - 1) * int(rows)
        end = (int(page) - 1) * int(rows) + int(rows)

        total = orders.count()
        orders = orders[start:end]

        dict = []
        resultdict = {}

        for tmp in orders:
            dic = {}
            dic['id'] = tmp.id
            dic['orderid'] = tmp.orderid
            dic['customer'] = tmp.customer.name
            dic['contact'] = tmp.contact
            dic['phone'] = tmp.phone
            dic['deposit'] = tmp.deposit
            dic['price'] = tmp.price
            dic['effectdays'] = tmp.effectdays
            dic['balance'] = tmp.balance
            dic['comment'] = tmp.comment
            dic['orderdate'] = tmp.orderdate.strftime("%Y-%m-%d")
            dict.append(dic)

        resultdict['code'] = 0
        resultdict['msg'] = ""
        resultdict['count'] = total 
        resultdict['data'] = dict

        return JsonResponse(resultdict, safe=False) 

class OrderAddPageView(LoginRequiredMixin, CreateView):
    login_url = "/account/login/"
    template_name = "order/order-add.html"
    ## fileds为页面上的表单要显示的项
    ##fields = ['orderid', 'customer', 'contact', 'phone', 'deposit',
    ##          'price', 'comment']

    ##Note1 此处只能使用这个,因为要返回customers做为下拉列表的内容 
    def get(self, request):
        customers = CustomerModel.objects.all()
        return render(request, "order/order-add.html", {"customers":customers})
    
    ##Note2 当继承的是CreateView时使用这个,功能与Note1是一样的,只是两种不同的实现方式
    ##queryset = OrderModel.objects.all()

    def post(self, request, *args, **kwargs):
        formObj = OrderAddForm(request.POST)
        resultdict = {}

        if formObj.is_valid():
            form_cd = formObj.cleaned_data 

            new_order = formObj.save(commit=False) ## form.save(commit=False)返回的是一个Model对象

            new_order.effectdays = new_order.get_effect_days()
            new_order.balance = new_order.get_balance()
            new_order.save(form_cd)

            resultdict['code'] = 0
            resultdict['msg'] = ""
            return JsonResponse(resultdict, safe=False) 
        else:
            print ("===================xxxx",formObj.errors)

        return self.render_to_response({"form":formObj})

class OrderDelPageView(LoginRequiredMixin, DeleteView):
    login_url = "/account/login/"
    success_url = reverse_lazy('order:show_orderList')

    model = OrderModel

    def delete(self, request, *args, **kwargs):
        ##for k, v in kwargs.items():
        ##    print ('%s，%s；' , (k, v))
        super(OrderDelPageView, self).delete(request, *args, **kwargs)
        return JsonResponse({'code':0, 'msg':''}) 

##class OrderDetailPageView(LoginRequiredMixin, DeleteView):
##    template_name = "order/order-update.html"
##    context_object_name = "order"
##
##    model = OrderModel
##
##    ##如果不要下边的这个函数,是不会把信息返回到表单的
##    ##def get_object(self, queryset=None):
##    ##    obj = super(OrderDetailPageView, self).get_object()
##    ##    return obj
##
##    ##下边注释的两个函数其实放开效果是一样的,只不过是记录一下怎么取url中的参数的方法
##    ##def get_object(self,queryset=None):
##    ##    obj_id = int(self.kwargs.get(self.pk_url_kwarg, None))
##    ##    obj = self.model.objects.get(id = obj_id)
##    ##    return obj 
##    
##    def get_context_data(self, **kwargs):
##        context = super(OrderDetailPageView, self).get_context_data(**kwargs)
##        return context
##
class OrderUpdatePageView(LoginRequiredMixin, UpdateView):
    login_url = "/account/login/"
    success_url = reverse_lazy('order:show_orderList')

    template_name = "order/order-update.html"
    template_name_suffix = '_update_form'
    fields = ['contact', 'phone', 'deposit', 'price', 'comment']
    context_object_name = "order"

    model = OrderModel

    ##def get_form_kwargs(self):
    ##    kwargs = super(OrderUpdatePageView,self).get_form_kwargs()
    ##    print ("==============kwargs id", self.kwargs['pk'])
    ##    return kwargs

    def post(self, request, *args, **kwargs):
        formObj = OrderAddForm(request.POST)
        resultdict = {}

        if formObj.is_valid():
            form_cd = formObj.cleaned_data 

            order = OrderModel.objects.get(id=self.kwargs['pk']) 
            order.contact = form_cd['contact']  
            order.phone = form_cd['phone']  
            order.deposit = form_cd['deposit']  
            order.price = form_cd['price']
            order.orderdate = form_cd['orderdate']

            order.effectdays = order.get_effect_days()
            order.balance = order.get_balance()

            order.save()

            resultdict['code'] = 0
            resultdict['msg'] = ""
            return JsonResponse(resultdict, safe=False) 
        else:
            print ("===================xxxx",formObj.errors)

        return self.render_to_response({"form":formObj})
####END: Add by SRJ-SGL 
