from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class Vacancy:
    """Класс для работы с вакансиями"""

    __slots__ = ["title", "url", "salary", "description", "requirements"]

    def __init__(
        self, title: str, url: str, salary: Optional[Dict[str, Optional[int]]], description: str, requirements: str
    ) -> None:
        """
        Инициализация объекта вакансии
        :param title: Название вакансии
        :param url: Ссылка на вакансию
        :param salary: Зарплата (словарь с ключами 'from', 'to', 'currency')
        :param description: Описание вакансии
        :param requirements: Требования к кандидату
        """
        self.title = self.__validate_title(title)
        self.url = self.__validate_url(url)
        self.salary = self.__validate_salary(salary)
        self.description = description
        self.requirements = requirements

    def __validate_title(self, title: str) -> str:
        """Валидация названия вакансии"""
        if not title:
            raise ValueError("Название вакансии не может быть пустым")
        return title

    def __validate_url(self, url: str) -> str:
        """Валидация URL вакансии"""
        if not url.startswith("http"):
            raise ValueError("URL вакансии должен начинаться с http/https")
        return url

    def __validate_salary(self, salary: Optional[Dict[str, Optional[int]]]) -> Dict[str, Optional[int]]:
        """Валидация зарплаты"""
        if salary is None:
            return {"from": None, "to": None, "currency": "RUR"}

        return {"from": salary.get("from"), "to": salary.get("to"), "currency": salary.get("currency", "RUR")}

    @property
    def avg_salary(self) -> float:
        """Средняя зарплата для сравнения"""
        from_val = self.salary["from"] or 0
        to_val = self.salary["to"] or 0
        return (from_val + to_val) / 2

    def __eq__(self, other: object) -> bool:
        """Проверка на равенство по зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other: object) -> bool:
        """Проверка на меньше по зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other: object) -> bool:
        """Проверка на меньше или равно по зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: object) -> bool:
        """Проверка на больше по зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: object) -> bool:
        """Проверка на больше или равно по зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        salary_from = self.salary["from"] if self.salary["from"] is not None else "не указана"
        salary_to = self.salary["to"] if self.salary["to"] is not None else "не указана"
        currency = self.salary["currency"] if self.salary["currency"] else ""
        return (
            f"Вакансия: {self.title}\n"
            f"Ссылка: {self.url}\n"
            f"Зарплата: от {salary_from} до {salary_to} {currency}\n"
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразование списка словарей в список объектов Vacancy"""
        vacancies: List[Vacancy] = []
        for vacancy_data in vacancies_data:
            try:
                vacancy = cls(
                    title=vacancy_data.get("name", ""),
                    url=vacancy_data.get("alternate_url", ""),
                    salary=vacancy_data.get("salary"),
                    description=vacancy_data.get("snippet", {}).get("responsibility", ""),
                    requirements=vacancy_data.get("snippet", {}).get("requirement", ""),
                )
                vacancies.append(vacancy)
            except (ValueError, KeyError):
                continue
        return vacancies
