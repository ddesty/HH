import json
import os
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List

from src.vacancy import Vacancy


class BaseSaver(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        """Получение вакансий из файла по критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из файла"""
        pass


class JSONSaver(BaseSaver):
    """Класс для работы с JSON-файлами"""

    def __init__(self, filename: str = "data/vacancies.json"):
        self.__filename = filename
        self.__ensure_directory_exists()
        self.__initialize_file()

    def __ensure_directory_exists(self) -> None:
        """Создает директорию для файла, если она не существует"""
        os.makedirs(os.path.dirname(self.__filename), exist_ok=True)

    def __initialize_file(self) -> None:
        """Инициализирует файл, если он не существует"""
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def __read_vacancies(self) -> List[Dict[str, Any]]:
        """
        Чтение вакансий из файла
        Обрабатывает различные кодировки и пустые файлы
        """
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                content = f.read()
                return json.loads(content) if content.strip() else []
        except (UnicodeDecodeError, json.JSONDecodeError):
            try:
                with open(self.__filename, "r", encoding="cp1251") as f:
                    content = f.read()
                    return json.loads(content) if content.strip() else []
            except Exception as e:
                print(f"Ошибка чтения файла: {e}")
                return []

    def __write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Запись вакансий в файл в UTF-8"""
        try:
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(vacancies, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка записи файла: {e}")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл, если она не существует"""
        vacancies = self.__read_vacancies()

        # Проверка на дубликаты по URL
        if not any(v["url"] == vacancy.url for v in vacancies):
            vacancies.append(
                {
                    "title": vacancy.title,
                    "url": vacancy.url,
                    "salary": vacancy.salary,
                    "description": vacancy.description,
                    "requirements": vacancy.requirements,
                }
            )
            self.__write_vacancies(vacancies)

    def get_vacancies(self, criteria: Dict[str, Any] = None) -> List[Vacancy]:
        """Возвращает отфильтрованные вакансии"""
        if criteria is None:
            criteria = {}

        vacancies_data = self.__read_vacancies()
        filtered_data = []

        for vacancy_data in vacancies_data:
            match = True
            for key, value in criteria.items():
                if key == "salary_from":
                    if vacancy_data["salary"]["from"] < value:
                        match = False
                elif key == "salary_to":
                    if vacancy_data["salary"]["to"] > value:
                        match = False
                elif key == "keyword":
                    if (
                        value.lower() not in vacancy_data["title"].lower()
                        and value.lower() not in vacancy_data["description"].lower()
                        and value.lower() not in vacancy_data["requirements"].lower()
                    ):
                        match = False
                elif vacancy_data.get(key) != value:
                    match = False

            if match:
                filtered_data.append(vacancy_data)

        return Vacancy.cast_to_object_list(filtered_data)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из файла"""
        vacancies = self.__read_vacancies()
        vacancies = [v for v in vacancies if v["url"] != vacancy.url]
        self.__write_vacancies(vacancies)
