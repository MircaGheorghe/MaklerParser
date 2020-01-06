from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from robot.models import *
from .forms import NameForm

# Create your views here.
def index(request):
    return render(request, 'robot/index.html', {
        'condition': mustPosted.objects.last(),
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all(),
        'form':NameForm(),
        })


def start_parser(request):
    condition = mustPosted.objects.last()
    condition.content = not condition.content
    condition.save()

    return redirect('home')



def set_category(request):
    if request.method == 'POST':
        cat = request.POST.get('cat')
        categorys = Category()
        categorys.content = cat
        categorys.save()
    return redirect('home')

def set_account(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('pass')
        author = request.POST.get('author')

        acc = Account()
        acc.author_id = author
        acc.username = login
        acc.password = password
        acc.save()
    return redirect('home')

def set_link(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        cont = request.POST.get('cont')
        category = request.POST.get('category')
        pay = request.POST.get('payment')

        newLink = Link()
        newLink.content = link
        newLink.account_id = cont
        newLink.category_id = category
        if not pay == None:
            newLink.payment = True
        else:
            newLink.payment = False

        newLink.save()
    return redirect('home')
