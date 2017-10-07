# coding: utf-8
import json

import datetime
from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,render_to_response
from TestModel.models import Test,NewBook,NewAuthor
def FirstView(request):
    context={}
    context['value']="Value setup"
    return render(request,'firstview.html',context)
    #re turn HttpResponse("First View")

def dbshow(request):
    test=Test.objects.all()
    return render(request,'db.html',{'teststr':test})

def books(request):
    authors=NewAuthor.objects.all()
    return render_to_response('books.html',{'authors':authors})

def showdate(request):
    return render_to_response('show_page.html', {'current_date': '2017 Sep'})


def ajax_list(request):
    a = range(100)
    return HttpResponse(json.dumps(a), content_type='application/json')


def ajax_dict(request):
    name_dict = {'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'}
    return HttpResponse(json.dumps(name_dict), content_type='application/json')


def show_string(request):
    return HttpResponse("A or B")


def getAgent(request):
    header=request.META['HTTP_USER_AGENT']
    return HttpResponse(header)

def notfound(request):
    return HttpResponseNotFound('not found!!!')

def time_show(request):
    now= datetime.datetime.now().strftime('%Y-%m-%d')
    html='''
    <html>
    <head>
    <title>
    This is title
    </title>
    </head>
    <body>
    <h1>%s</h1>
    </body>
    </html>
    ''' %now

    return HttpResponse(html)
