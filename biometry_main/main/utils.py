from django.core.files.storage import default_storage
import os, json, hashlib
from datetime import datetime
from web_biometry import settings
from json import JSONEncoder
import numpy



def save(file_name: str, audio_file) -> None:
    '''
    Функция сохранения файла в указанный каталог
    '''
    with default_storage.open(file_name, 'wb+') as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)

def get_temp_filename(seed: str = '') -> str:
    '''
    Возвращает случаное имя временного файла
    '''
    date = bytes((datetime.now().isoformat() + seed).encode('utf-8'))
    return os.path.join(settings.VOICE_FILES, hashlib.md5(date).hexdigest() + '.wav')

def remove_file(file_name: str) -> None:
    '''
    Функция удаления файла
    '''
    if os.path.exists(file_name): os.remove(file_name)

    
class NumpyArrayEncoder(JSONEncoder):
    '''
    Класс для сериализации массива numpy в json
    '''
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)