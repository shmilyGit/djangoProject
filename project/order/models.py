from django.db import models
from django import forms
from django.conf import settings
from customer.models import CustomerModel

import datetime

# Create your models here.

class OrderModel(models.Model):
    orderid = models.CharField(max_length=24, blank=False, null=False)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, blank=False, null=False, related_name='rn_Order_Customer')
    contact = models.CharField(max_length=24, blank=False, null=False)
    phone = models.CharField(max_length=11, default=False, null=False)

    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    effectdays = models.PositiveSmallIntegerField(blank=True, null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    comment = models.CharField(max_length=100, blank=True, null=True)
    orderdate = models.DateTimeField(blank=False, null=False)

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return 'order:{},{},{},{},{},{},{}'.format(self.orderid, self.customer, self.contact,self.deposit, self.price, self.effectdays, self.balance)
    
    def get_effect_days(self):
        date_format = "%m/%d/%Y"
        now = datetime.datetime.now()
        delta = now - self.orderdate
        return delta.days + 1

    def get_balance(self):
        balance = self.deposit - self.price * self.get_effect_days() 
        return balance

    def get_after7days_expire(self):
        if self.balance < self.price * 7 :
            return 1 
        else:
            return 0

    def get_after7days_expire(self):
        if self.balance < self.price * 3 :
            return 1 
        else:
            return 0

    def get_expired(self):
        if self.balance < 0 :
            return 1 
        else:
            return 0
