from django.urls import path
from . import views
import os, json, numpy as np
from web_biometry import settings
from .models import samples
from Recognizer import Recognizer

# Проверка на существование папки для временных файлов
if not os.path.exists(settings.VOICE_FILES): 
    os.mkdir(settings.VOICE_FILES)
    print('Created ' + settings.VOICE_FILES)

# Проверка на существование файла модели. В случае отсутствия переобучение из БД
if not os.path.exists(settings.DEFAULT_MODEL_FILE): 
    recognizer = Recognizer.Recognizer(settings.DEFAULT_MODEL_FILE)
    for sample in samples.objects.all():
        features = json.loads(sample.features)
        features = np.asanyarray(features)
        recognizer.save(sample.id_user.username, features)
    recognizer.train()
    recognizer.save_model()

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("login/verification/", views.verification_login),
    path("login/verification/GIS", views.gis),
    path("login/verification/critical", views.critical),
    path("login/verification/user_login_critical", views.user_login_critical),
    path("registration", views.registration, name="registration"),
    path("registration/verification", views.verification),
    path("registration/verification/complete_registration", views.complete_reg),
    path("registration/verification/critical", views.critical),
    path("registration/verification/user_use", views.user_use)
]