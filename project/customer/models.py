from django.db import models
from django.conf import settings

# Create your models here.

class CustomerModel(models.Model):
    customer = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=24, blank=True)
    phone = models.CharField(max_length=11, default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-id',)
    
    def __str__(self):
        return 'customer:{},{},{}'.format(self.customer, self.contact, self.phone, self.created)
