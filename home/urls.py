from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name = "home"),
    # path('about', views.about, name = "about"),
    # path('addNote', views.addNote, name = "addNote"),
    # path('contact', views.contact, name = "contact"),
    # path('signup', views.signup, name = "signup"),
    # path('login', views.loginUser, name = "login"),
    # path('logout', views.logoutUser, name = "login"),
]
