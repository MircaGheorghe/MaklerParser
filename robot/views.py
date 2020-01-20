from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from subprocess import Popen
from .forms import NameForm
from robot.models import *
import os

# Create your views here.
@login_required(login_url='/admin/login/?next=/') #redirect when user is not logged in
def index(request):
    user = request.user
    accounts = user.account_user.all
    return render(request, 'robot/index.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'is_work': mustPosted.objects.last(),
        'users': User.objects.all(),
        'current_user': user.id,
        'account':accounts,
        'form':NameForm(),
        })



def page_logout(request):
    logout(request)
    return redirect('home')


def change_status(request):
    print(1, '!!!!!!!!!!!!')
    condition = mustPosted.objects.last()
    print(2, '!!!!!!!!!!!!')
    condition.content = not condition.content
    print(3, '!!!!!!!!!!!!')
    condition.save()
    print(4, '!!!!!!!!!!!!')
    if condition.content == True:
        print(5, '!!!!!!!!!!!!')
        try:
            print(6, '!!!!!!!!!!!!')
            proc = Popen(["python manage.py robot"], shell=True)
        except:
            print(7, '!!!!!!!!!!!!')
            proc = Popen("/home/env/bin/python /home/makler-publication/manage.py robot", shell=True)
    data = {
        "status": condition.content
    }
    return JsonResponse(data)




# Salveaza o noua categorie in baza de date
def set_category(request):
    cont = request.GET.get('rez', None)
    cat_name = request.GET.get('name', None)
    categorys = Category()
    categorys.content = cont
    categorys.name = cat_name
    categorys.save()
    return HttpResponse(200)



#Salveaza un nou cont in baza de date
def set_account(request):
    login = request.GET.get('login', None)
    password = request.GET.get('pass', None)
    author = request.GET.get('author', None)

    acc = Account()
    acc.author_id = author
    acc.username = login
    acc.password = password
    acc.save()
    return HttpResponse(status = 200)


# Sllveaza un nou link a unui post in baza de date
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

    return HttpResponse(200)


def delete_acc(request):
    id = request.GET.get('id', None)
    Account.objects.filter(id=id).delete()
    return HttpResponse(200)

def delete_link_cat(request):
    id = request.GET.get('id', None)
    if(id[-1] == 'c'):
        id = id[:-1]
        Category.objects.filter(id=id).delete()
    if(id[-1] == 'l'):
        id = id[:-1]
        Link.objects.filter(id=id).delete()

    return HttpResponse(200)


def get_modal(request):
    return render(request, 'robot/modal_link.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        })

def get_table(request):
    return render(request, 'robot/table.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'form':NameForm(),
        })

def get_acc_modal(request):
    return render(request, 'robot/modal_get_acc.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        })

