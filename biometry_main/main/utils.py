from django.core.files.storage import default_storage
import os
import hashlib
from datetime import datetime
from web_biometry import settings


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