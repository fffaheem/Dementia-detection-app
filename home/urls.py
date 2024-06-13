from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('login', views.loginUser, name = "login"),
    path('signup', views.signup, name = "signup"),
    path('logout', views.logoutUser, name = "logout"),
    path('user', views.user, name = "user"),
    path('contactus', views.contactus, name = "contactus"),

    # path('about', views.about, name = "about"),
    # path('addNote', views.addNote, name = "addNote"),
    # path('contact', views.contact, name = "contact"),
    # path('logout', views.logoutUser, name = "login"),
]
