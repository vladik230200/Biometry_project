from django.shortcuts import render
from django.http import JsonResponse
from main.models import users, samples
import hashlib
import string
import json
import base64
import numpy as np
from . import utils
from Recognizer import Recognizer
from web_biometry import settings

def critical(request):
    render(request, "main/critical_404.html")

def index(request):
    print(utils.get_temp_filename())
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'main/login.html')

def registration(request):
    return render(request, 'main/registration.html')

def critical(request):
    return render(request, "main/critical_404.html")

def complete_reg(request):
    return render(request, "main/complete_registration.html")

def user_use(request):
    return render(request, "main/user_use.html")

def user_login_critical(request):
    return render(request, "main/user_login_critical.html")

def gis(request):
    return render(request, "main/GIS.html")

def password_hash(password_sha):
    bytes_password = bytes(password_sha.encode("utf-8"))
    password_sha = hashlib.sha256(bytes_password).hexdigest()
    return password_sha

def verification(request):
    if request.method == 'POST':
        csrf_token = request.POST['csrfmiddlewaretoken']
        login_user = request.POST["login"].translate({ord(c): None for c in string.whitespace})
        password_user = request.POST["password"].translate({ord(c): None for c in string.whitespace})
        audio = request.FILES
        sample_massiv = []
        for seed in range(len(audio)):
            sample = audio["audio" + str(seed + 1)]
            sample_massiv.append(sample)
        login_user_check = users.objects.filter(username=login_user)
        # login_user_check = [] # For debug
        if len(login_user) <= 0 or len(password_user) <= 0 or len(sample_massiv) < 3:
            data = {"redirect_url" : "registration/verification/critical"}
            return JsonResponse(data)
        else:
            if len(login_user_check) == 0:
                users(username = str(login_user), password = str(password_hash(password_user)), voice = False).save()
                # TODO 
                # Можно доделать логику с 5 секундными семплами
                seed = 0
                recognizer = Recognizer.Recognizer(settings.DEFAULT_MODEL_FILE)
                for file in sample_massiv:
                    seed = seed + 1
                    file_name = utils.get_temp_filename(str(seed))
                    utils.save(file_name, file)
                    features = recognizer.extract_features(file_name)
                    sample = samples()
                    sample.id_user = users.objects.filter(username=login_user)[0]
                    sample.features = json.dumps(features, cls=utils.NumpyArrayEncoder)
                    # TODO не сохраняет бинарно, но возвращает b''
                    sample.sample = file.read()
                    sample.save()
                    utils.remove_file(file_name)
                # Переобучение модели
                for sample in samples.objects.all():
                    features = json.loads(sample.features)
                    features = np.asanyarray(features)
                    recognizer.save(sample.id_user.username, features)
                recognizer.train()
                recognizer.save_model()

                data = {"redirect_url": "registration/verification/complete_registration"}
                return JsonResponse(data)
            else:
                data = {"redirect_url": "registration/verification/user_use"}
                return JsonResponse(data)

def verification_login(request):
    if request.method == 'POST':
        csrf_token = request.POST['csrfmiddlewaretoken']
        login_user = request.POST["login"].translate({ord(c): None for c in string.whitespace})
        password_user = request.POST["password"].translate({ord(c): None for c in string.whitespace})
        audio = request.FILES
        sample_massiv = []
        for i in range(len(audio)):
            sample = audio["audio" + str(i + 1)]
            sample_massiv.append(sample)
        if len(login_user) <= 0 or len(password_user) <= 0 or (len(sample_massiv) < 1 or (len(sample_massiv)) > 1):
            data = {"redirect_url": "login/verification/critical"}
            return JsonResponse(data)
        else:
            user_by_login_sql = users.objects.filter(username=login_user)
            if len(user_by_login_sql) <= 0:
                data = {"redirect_url": "login/verification/user_login_critical"}
                return JsonResponse(data)
            else:
                if (user_by_login_sql[0].username == login_user and \
                        user_by_login_sql[0].password == password_hash(password_user)):
                    recognizer = Recognizer.Recognizer(settings.DEFAULT_MODEL_FILE)
                    file_name = utils.get_temp_filename()
                    utils.save(file_name, sample_massiv[0])
                    recognizer.load_model()
                    features = recognizer.extract_features(file_name)
                    utils.remove_file(file_name)
                    if recognizer.verify(login_user, features):
                        data = {"redirect_url": "login/verification/GIS"}
                        return JsonResponse(data)
                    else:
                        data = {"redirect_url": "login/verification/user_login_critical"}
                        return JsonResponse(data)
                else:
                    data = {"redirect_url": "login/verification/user_login_critical"}
                    return JsonResponse(data)
