from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from robot.models import *
from .forms import NameForm
from django.http import JsonResponse
import os

# Create your views here.
def index(request):
    return render(request, 'robot/index.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'is_work': mustPosted.objects.last(),
        'form':NameForm(),
        })



def change_text(request):
    condition = mustPosted.objects.last()
    condition.content = not condition.content
    condition.save()
    data = {
        'status': condition.content
    }
    return JsonResponse(data)

def start_parser(request):
    os.system("python manage.py robot")
    return HttpResponse(200)


# Functie pentru a salva o nou categorie in baza de date
def set_category(request):
    cont = request.GET.get('rez', None)
    cat_name = request.GET.get('name', None)
    categorys = Category()
    categorys.content = cont
    categorys.name = cat_name
    categorys.save()
    return render(request, 'robot/table.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'form':NameForm(),
        })



def set_account(request):
    login = request.GET.get('login', None)
    password = request.GET.get('pass', None)
    author = request.GET.get('author', None)

    acc = Account()
    acc.author_id = author
    acc.username = login
    acc.password = password
    acc.save()
    return render(request, 'robot/modal_link.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'form':NameForm(),
        })



def set_link(request):
    link = request.GET.get('link', None)
    cont = request.GET.get('cont', None)
    category = request.GET.get('category', None)
    cu_plata = request.GET.get('cu_plata', None)

    newLink = Link()
    newLink.content = link
    newLink.account_id = cont
    newLink.category_id = category
    if cu_plata == "true":
        newLink.payment = True
    else:
        newLink.payment = False
    newLink.save()

    return render(request, 'robot/table.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'form':NameForm(),
        })



def delete_link(request):
    id = request.GET.get('id', None)
    Link.objects.filter(id=id).delete()

    return render(request, 'robot/table.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'form':NameForm(),
        })
