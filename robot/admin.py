from django.contrib import admin
from .models import Account, Link, Category, mustPosted

# Register your models here.
admin.site.register(Account)
admin.site.register(Link)
admin.site.register(Category)
admin.site.register(mustPosted)
