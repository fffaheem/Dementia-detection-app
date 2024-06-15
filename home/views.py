from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from home.models import Contact, Diagnose
from django.utils import timezone
from django.shortcuts import get_object_or_404


@login_required(login_url="login")
def index(request):

    instance = request.user
    if request.method == "POST":
        email = instance.email
        username = instance.username
        text = "demented hai"
        cdr = 0.0
        cdr_text = "cognitive normal"
        image = request.FILES.get('image')
        time = timezone.now()
        try:
            diagnose = Diagnose(username = instance, email=email, text=text, image=image,cdr = cdr, cdr_text = cdr_text ,datetime=time)
            diagnose.save()
            # print("id is "+str(diagnose.id))
            # print("success")
            messages.success(request, "Success",extra_tags="success index")
            return redirect(f"/details?show=true&id={diagnose.id}")
        except:
            # print("Something went wrong")
            messages.error(request, "Something went wrong",extra_tags="danger index")
        # print(email,username,text,cdr,image)

    context = {
        "home_active" : "active"
    }
    return render(request,"index.html",context)

@login_required(login_url="login")
def user(request):
    instance = request.user

    if request.method == "GET" and request.GET.get("delete"):
        get_id = request.GET.get("id")
        d = get_object_or_404(Diagnose,id=get_id)
        print(d.username)
        if d.username == instance:
            d.delete()
            messages.success(request, "deleted successfully",extra_tags="success user")
        else:
            messages.error(request, "not yours to delete",extra_tags="danger user")

        

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
    scans = Diagnose.objects.filter(username=instance)
    context = {
        "user_active" : "active",
        "username" : username,
        "email" : email,
        "firstname" : firstname,
        "lastname" : lastname,
        "scans" : scans,
    }
    return render(request,"user.html",context)

@login_required(login_url="login")
def details(request):
    instance = request.user
    if request.method == "GET" and request.GET.get("show"):
        get_id = request.GET.get("id")
        d = get_object_or_404(Diagnose,id=get_id)
        if d.username == instance:
            context = {
                "scan":d
            }
            return render(request,"details.html",context)
        else: 
            return redirect("/")
    else:
        return redirect("/")

def contactus(request):

    if request.method == "POST":
        email = request.POST.get("email")
        text = request.POST.get("text")
        time = datetime.today()
        try:
            contact = Contact(email=email, text=text, date=time)
            contact.save()            
            messages.success(request, "query send successfully.",extra_tags="success contact")
        except:
            messages.error(request, "Oops something went wrong.",extra_tags="danger contact")


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