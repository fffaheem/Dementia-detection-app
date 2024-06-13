from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from home.models import Contact


@login_required(login_url="login")
def index(request):
    context = {
        "home_active" : "active"
    }
    return render(request,"index.html",context)

@login_required(login_url="login")
def user(request):
    instance = request.user

    if request.method == "POST":
        post_email = request.POST.get("email")
        post_username = request.POST.get("username")
        post_first = request.POST.get("first")
        post_last = request.POST.get("last")
        try:
            instance.username = post_username
            instance.email = post_email
            instance.first_name = post_first
            instance.last_name = post_last
            instance.save()
            messages.success(request, "Account updated successfully.",extra_tags="success user")
        except:
            messages.error(request, "Username already exists.",extra_tags="danger user")
        

    email = instance.email
    id = instance.id
    username = instance.username
    firstname = instance.first_name
    lastname = instance.last_name

    context = {
        "user_active" : "active",
        "username" : username,
        "email" : email,
        "firstname" : firstname,
        "lastname" : lastname
    }
    return render(request,"user.html",context)

def contactus(request):

    if request.method == "POST":
        email = request.POST.get("email")
        text = request.POST.get("text")
        time = datetime.today()
        print(email,text,time)


    context = {
        "contactus_active" : "active"
    }
    return render(request,"contactus.html",context)



def loginUser(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        user = authenticate(username=username, password = password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            print("not logged in")

    context = {
        "login_active" : "active"
    }
    return render(request,"login.html",context)

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        first = request.POST.get("first")
        last = request.POST.get("last")
        password = request.POST.get("password")
        try:
            user = User.objects.create_user(email = email, username=username, first_name= first, last_name=last, password=password)
            user.save()
            messages.success(request, "Account Created Successfully.",extra_tags="success signup")
            return redirect("/login")
        except:
            messages.error(request, "Username or email already exists.", extra_tags="danger signup")


    context = {
        "login_active" : "active"
    }

    return render(request,"signup.html",context)

def logoutUser(request):
    
    logout(request)
    return redirect("/login")