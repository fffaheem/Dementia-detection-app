from django.shortcuts import render

# Create your views here.

def index(request):
    # return HttpResponse("home s hoo")
    return render(request,"index.html")