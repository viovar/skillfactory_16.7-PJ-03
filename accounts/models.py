# Create your models here.
from django.db import models
from django.contrib.auth.models import User



class UsersAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.SmallIntegerField(default=0)




class OneTimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=6, blank=True, null=True)
