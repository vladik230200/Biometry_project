import os, json, numpy as np
from web_biometry import settings
from main.models import samples
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
