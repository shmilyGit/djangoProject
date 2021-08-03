from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='rn_UserInfo')
    name = models.CharField(max_length=20, blank=True)
    gender = models.BooleanField(default=True)
    birth = models.DateField(blank=True, null=True)
    website = models.URLField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    comment = models.TextField(max_length=100, blank=True)
    photo = models.ImageField(blank=True)

    def __str__(self):
        return 'user:{},{},{}'.format(self.user.username, self.name, self.phone)

# Create your models here.
