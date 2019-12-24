from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Link(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    content = models.TextField()
    payment = models.BooleanField(default=False)
    post_date = models.DateTimeField(null = True, blank = True)

class Category(models.Model):
    content = models.CharField(max_length=400)

