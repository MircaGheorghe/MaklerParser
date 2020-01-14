from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from robot.models import *
from .forms import NameForm
from django.http import JsonResponse
import os
from django.contrib.auth.decorators import login_required
from django.core.management import call_command

# Create your views here.
@login_required(login_url='/admin/login/?next=/') #redirect when user is not logged in
def index(request):
    return render(request, 'robot/index.html', {
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'is_work': mustPosted.objects.last(),
        'users': User.objects.all(),
        'form':NameForm(),
        })



def change_text(request):
    condition = mustPosted.objects.last()
    condition.content = not condition.content
    condition.save()
    if condition.content == True:
        call_command('robot')
    data = {
        'status': condition.content
    }
    return JsonResponse(data)




# Functie pentru a salva o nou categorie in baza de date
def set_category_table(request):
    cont = request.GET.get('rez', None)
    cat_name = request.GET.get('name', None)
    categorys = Category()
    categorys.content = cont
    categorys.name = cat_name
    categorys.save()
    return HttpResponse(200)



# Functie pentru a salva o nou categorie in baza de date/reinnoirea modalului
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

def delete_link(request):
    id = request.GET.get('id', None)
    Link.objects.filter(id=id).delete()

    return HttpResponse(200)
