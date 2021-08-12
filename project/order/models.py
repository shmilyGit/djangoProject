from django.db import models
from django.conf import settings
from customer.models import CustomerModel

# Create your models here.

class OrderModel(models.Model):
    orderid = models.CharField(max_length=24, blank=False)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE, related_name='rn_Order_Customer')
    contact = models.CharField(max_length=24, blank=False)
    phone = models.CharField(max_length=11, default=False)

    deposit = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    days = models.PositiveSmallIntegerField(blank=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    comment = models.CharField(max_length=100, blank=True)
    orderdate = models.DateTimeField(blank=False)

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return 'customer:{},{},{}'.format(self.customer, self.contact, self.phone, self.created)
