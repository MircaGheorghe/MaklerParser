from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Account(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_user')
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Link(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='link_account')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1, related_name='link_category')
    content = models.TextField()
    payment = models.BooleanField(default=False)
    posted = models.BooleanField(default=False)
    post_date = models.DateTimeField(null = True, blank=True)

class Category(models.Model):
    content = models.CharField(max_length=400)
    name = models.CharField(max_length=400, default="name")

class mustPosted(models.Model):
    content = models.BooleanField(default=False)