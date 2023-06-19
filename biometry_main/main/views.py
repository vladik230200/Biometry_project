from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from main.models import users, samples
import hashlib
import string
import io
import wave
import librosa
import scipy.io.wavfile as wavfile
import numpy as np

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
        for i in range(len(audio)):
            sample = audio["audio" + str(i + 1)]
            sample_massiv.append(sample)
        for i, sample_blob in enumerate(sample_massiv):
            # Прочитать данные из объекта InMemoryUploadedFile
            data = sample_blob.read()
            # Уменьшить размер данных до ближайшего кратного размеру элемента
            data_size = len(data)
            element_size = np.dtype(np.int16).itemsize
            new_data_size = data_size - (data_size % element_size)
            data = data[:new_data_size]
            # Преобразовать данные в формат wav и сохранить их в файл
            sr = 16000
            wav_data = np.frombuffer(data, dtype=np.int16)
            wavfile.write("wave" + str(i) + ".wav", sr, wav_data)

        """
        for i in range(len(audio)):
            audio_data = audio["audio" + str(i+1)]
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_data.read()))
            audio_segment.export('audio.wav', format='wav')
        """

        """
        for i in range(len(audio)):
            audio_data = audio["audio" + str(i + 1)].read()  # читаем данные из InMemoryUploadedFile
            sample = memoryview(audio_data).cast('B')  # преобразуем в байты
            print(sample)
            with wave.open('audio' + str(i + 1) + '.wav', 'wb') as wav_file:
                # Устанавливаем параметры записи: монофонический звук, частота дискретизации 44100 Гц, 16 бит на сэмпл
                wav_file.setnchannels(1)
                wav_file.setframerate(44100)
                wav_file.setsampwidth(2)
                # Запись данных в файл
                wav_file.writeframes(audio_data)
                # Запись заголовка WAV-файла
                wav_file.writeframesraw(b'')
                # Закрытие файла
                wav_file.close()
        """



        login_user_check = users.objects.filter(username=login_user)
        if len(login_user) <= 0 or len(password_user) <= 0 or len(sample_massiv) < 3:
            data = {"redirect_url" : "registration/verification/critical"}
            return JsonResponse(data)
        else:
            if len(login_user_check) == 0:
                users(username = str(login_user), password = str(password_hash(password_user)), voice = False).save()
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
                    data = {"redirect_url": "login/verification/GIS"}
                    return JsonResponse(data)
                else:
                    data = {"redirect_url": "login/verification/user_login_critical"}
                    return JsonResponse(data)