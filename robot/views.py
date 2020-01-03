from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from robot.models import *

# Create your views here.
def index(request):
    return render(request, 'robot/index.html', {
        'condition': mustPosted.objects.last(),
        'account': Account.objects.all(),
        'category': Category.objects.all(),
        'links':Link.objects.all()
        })


def start_parser(request):
    condition = mustPosted.objects.last()
    condition.content = not condition.content
    condition.save()

    return redirect('home')