from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse

def critical(request):
    render(request, "main/critical_404.html")

def index(request):
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'main/login.html')

def registration(request):
    return render(request, 'main/registration.html')

def critical(request):
    return render(request, "main/critical_404.html")

def complete_reg(request):
    return render(request, "main/complete_registration.html")

def verification(request):
    if request.method == 'POST':
        csrf_token = request.POST['csrfmiddlewaretoken']
        login_user = request.POST["login"]
        password_user = request.POST["password"]
        audio = request.FILES["audio"]
        if len(login_user) <= 0 or len(password_user) <= 0:
            data = {"redirect_url" : "registration/verification/critical"}
            return JsonResponse(data)
        else:
            data = {"redirect_url": "registration/verification/complete_registration"}
            return JsonResponse(data)

def verification_login(request):
    return 1

def gis(request):
    return render(request, "main/GIS.html")