from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List

import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def connect(self) -> None:
        """Метод для подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Метод для получения вакансий по ключевому слову"""
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 10}

    def connect(self) -> None:
        """Подключение к API HeadHunter"""
        response = requests.get(self.__base_url, headers=self.__headers)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка подключения к API HH: {response.status_code}")

    def get_vacancies(self, keyword: str) -> List[Dict[str, Any]]:
        """Получение вакансий по ключевому слову"""
        if not hasattr(self, "_HeadHunterAPI__params"):
            self.__params = {"text": "", "page": 0, "per_page": 100}

        self.connect()
        self.__params["text"] = keyword
        vacancies = []

        # Проверяем флаг тестового режима
        test_mode = self.__params.pop("_test_mode", False)

        if test_mode:
            # В тестовом режиме делаем только один запрос
            response = requests.get(self.__base_url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                return response.json().get("items", [])
            return []

        # Обычный режим работы (до 20 страниц)
        while self.__params.get("page") != 20:
            response = requests.get(self.__base_url, headers=self.__headers, params=self.__params)
            if response.status_code == 200:
                data = response.json()
                vacancies.extend(data.get("items", []))
                self.__params["page"] += 1
            else:
                break

        return vacancies
