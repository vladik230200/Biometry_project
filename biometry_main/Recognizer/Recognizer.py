from sklearn.ensemble import RandomForestClassifier
from typing import Tuple
import numpy as np
import librosa

class Recognizer:
    '''
    Класс для идентификации по голосу
    '''

    def __init__(self,
                model_file_name: str,
                predict_threshold: float = 0.5,
                features_count: int = 40) -> None:
        self.features = []
        self.logins = []
        self.model = None
        self.model_file_name = model_file_name
        self.predict_threshold = predict_threshold
        self.features_count = features_count
    
    def extract_features(self, file_name: str) -> np.ndarray:
        '''
        Функция выгрузки из .wav файла характеристик сингала

        Возвращает `ndarray(dtype=numpy.float32)`
        '''
        x, sr = librosa.load(file_name)
        mfccs = librosa.feature.mfcc(y=x, sr=sr, n_mfcc=self.features_count)
        return np.mean(mfccs, axis=1)

    def save(self, login: str, features) -> None:
        '''
        Функция созранения в модель логина и характеристик сигнала
        '''
        pass

    def train(self) -> None:
        '''
        Функция обучения модели на загруженных записях
        '''
        pass

    def predict(self, features) -> Tuple[str, int]:
        '''
        Функция предсказания голоса

        Возвращает предсказанный логин и вероятность предсказания
        '''
        pass

    def verify(self, login: str, features) -> bool:
        '''
        Функция для проверки голоса пользователя
        '''
        pass

    def save_model(self):
        '''
        Сохраненияе дампа модели в память
        '''
        pass

    def load_model(self):
        '''
        Выгрузка дампа модели из памяти
        '''
        pass

