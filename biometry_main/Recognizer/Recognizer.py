from sklearn.ensemble import RandomForestClassifier
from typing import Tuple
import numpy as np
import librosa, joblib

class Recognizer:
    '''
    Класс для идентификации по голосу
    '''

    def __init__(self,
                model_file_name: str,
                predict_threshold: float = 0.5,
                features_count: int = 40) -> None:
        self.features = []
        self.user_names = []
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

    def save(self, user_name: str, features: np.ndarray) -> None:
        '''
        Функция созранения в модель логина и характеристик сигнала
        '''
        self.user_names.append(user_name)
        self.features.append(features)

    def train(self) -> None:
        '''
        Функция обучения модели на загруженных записях
        '''
        self.model = RandomForestClassifier()
        self.model.fit(self.features*5, self.user_names*5)

    def predict(self, features: np.ndarray) -> Tuple[str, int]:
        '''
        Функция предсказания голоса

        Возвращает предсказанный логин и вероятность предсказания
        '''
        user_name = self.model.predict([features])[0]
        probabilty = np.max(self.model.predict_proba([features]))
        return user_name, probabilty

    def verify(self, user_name: str, features: np.ndarray) -> bool:
        '''
        Функция для проверки голоса пользователя
        '''
        user, probability = self.predict(user_name, features)
        return user_name == user and probability >= self.predict_threshold
    
    def save_model(self):
        '''
        Сохраненияе дампа модели в память
        '''
        joblib.dump(self.model, self.model_file_name)
        print('Model saved!')

    def load_model(self):
        '''
        Выгрузка дампа модели из памяти
        '''
        self.model = joblib.load(self.model_file_name)
        print('Model loaded')

