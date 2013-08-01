# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# import datetime,time
import urllib,urllib2,json,httplib2

def index(request):
    if request.user.is_authenticated():
        return render_to_response("index.html",{'user':request.user})
    else:
        return render_to_response("logon.html")

def logout(request):
    auth.logout(request)
    return render_to_response("logon.html")

def verifyUser(request):
    if 'username' in request.POST:
        usern = request.POST['username']
    else:
        usern = ''
    if 'password' in request.POST:
        passw = request.POST['password']
    else:
        passw = ''
    user = authenticate(username=usern, password=passw)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('home')
    else:
        return render_to_response('logon.html',{'error':"Please check your LOGIN information!"})

def register(request):
    return render_to_response("register.html")

def createUser(request):
    if 'username' in request.GET:
        username = request.GET.get('username')
    if 'password' in request.GET:
        password = request.GET.get('password')
    if 'email' in request.GET:
        email = request.GET.get('email')
	user = User.objects.create_user(username,email,password)
    return HttpResponse(1)

def favList(request):
    return render_to_response('favor.html',{'user':request.user})

def hotList(request):
    return render_to_response('hot.html',{'user':request.user})

# def connectLastFmDatabase(request):
#     cursor = connection['lastFm'].cursor()
#     cursor.execute('Create table Test(ID number, Name Text(30), Age number)')
#     cursor.execute('Insert into Test(ID, Name, Age) values(1, "wbs", 22)')
#     cursor.execute('Select Name from Test order by Name')
#     names = [row[0] for row in cursor.fetchall()]
#     connection.close
#     return cursor

# def connectMusicPushDatabase():
#     cursor = connection.cursor()
#     connection.close
#     return cursor
