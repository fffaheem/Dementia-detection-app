from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from home.models import Contact, Diagnose, AI
from django.utils import timezone
from django.shortcuts import get_object_or_404

from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

def is_image_valid_mri(validator_model,path,threshold):
    img = cv2.imread(path)
    resize = tf.image.resize(img, (32,32))
    model_prediction = validator_model.predict(np.expand_dims(resize/255,0))
    if model_prediction[0][0] > threshold:
        return "invalid"
    else:
        return "valid"
    
def check_for_dementia(model,path):
    img = cv2.imread(path)
    resize = tf.image.resize(img, (256,256))
    model_prediction = model.predict(np.expand_dims(resize/255,0))
    predicted_class = model_prediction.argmax(axis=1)[0]
   
    if predicted_class == 0:
        # return "0.0: Cognitively normal"
        return 0.0
    elif predicted_class == 1:
        # return "0.5: Questionable"
        return 0.5
    elif predicted_class == 2:
        return 1.0
    else:
        return 2.0

alzheimer_model = load_model(BASE_DIR / "AI model/CNN_images_only.h5")
validator_model = load_model(BASE_DIR / "AI model/images_validator3.h5")
# validator_model = load_model(os.path.join("images_validator3.h5"))




@login_required(login_url="login")
def index(request):
    instance = request.user
    if request.method == "POST":
        email = instance.email
        # username = instance.username
        text = "Your cognitive health is in excellent condition. No signs of dementia were detected. Continue maintaining a healthy lifestyle and regular check-ups to keep your brain healthy."
        cdr = 0.0
        cdr_text = "Cognitive normal"
        image = request.FILES.get('image')
        time = timezone.now()
        try:
            diagnose = Diagnose(username = instance, email=email, text=text, image=image,cdr = cdr, cdr_text = cdr_text ,datetime=time)
            diagnose.save()

            full_path = os.path.join(BASE_DIR,diagnose.image.url[1:])
            print(full_path)
            is_valid = is_image_valid_mri(validator_model,full_path,AI.objects.all()[0].threshold)
            if is_valid == "valid":
                cdr = check_for_dementia(alzheimer_model,full_path)
                print(cdr)
                cdr_text = ""
                cdr_long_text = ""
                if cdr == 0.0:
                    cdr_text = "Cognitive Normal"
                    cdr_long_text = "Your cognitive health is in excellent condition. No signs of dementia were detected. Continue maintaining a healthy lifestyle and regular check-ups to keep your brain healthy."
                elif cdr == 0.5:
                    cdr_text = "Questionable"
                    cdr_long_text = "There are some mild signs that may suggest early cognitive changes. It is important to monitor your health closely and consider consulting with a specialist to further evaluate your cognitive status and take preventive measures."
                elif cdr == 1.0:
                    cdr_text = "Mild"
                    cdr_long_text = "Mild cognitive impairment has been detected. This may impact your daily activities slightly. We recommend scheduling an appointment with a healthcare professional to discuss potential treatments and support options to help manage your condition."
                elif cdr == 2.0:
                    cdr_text = "Moderate or Severe"
                    cdr_long_text = "Moderate to severe cognitive impairment has been identified. This is likely to significantly impact your daily life. It is crucial to seek immediate medical advice to explore available treatments and support services. We are here to assist you and your loved ones through this journey."

                diagnose.cdr = cdr
                diagnose.cdr_text = cdr_text
                diagnose.text = cdr_long_text
                diagnose.save()
                messages.success(request, "Success",extra_tags="success index")
                return redirect(f"/details?show=true&id={diagnose.id}")
            else:
                diagnose.delete()
                if os.path.exists(full_path):
                    os.remove(full_path)
                messages.error(request, "Invalid MRI Image",extra_tags="danger index")
            # print(full_path)
            
        except:
            # print("Something went wrong")
            diagnose.delete()
            if os.path.exists(full_path):
                    os.remove(full_path)
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
    scans = Diagnose.objects.filter(username=instance).order_by('-datetime')
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
    if request.user.is_authenticated:
        return redirect("/")
    
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

    return render(request,"signup.html")

def logoutUser(request):
    
    logout(request)
    return redirect("/login")