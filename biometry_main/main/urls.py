from django.urls import path
from . import views

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