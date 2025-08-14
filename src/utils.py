from typing import List

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keyword: str) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевому слову
    :param vacancies: Список вакансий
    :param keyword: Ключевое слово для фильтрации
    :return: Отфильтрованный список вакансий
    """
    if not keyword:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Проверяем, что description не None перед вызовом lower()
        description = vacancy.description or ""
        requirements = vacancy.requirements or ""

        if (
            keyword.lower() in vacancy.title.lower()
            or keyword.lower() in description.lower()
            or keyword.lower() in requirements.lower()
        ):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтрация вакансий по диапазону зарплат
    :param vacancies: Список вакансий
    :param salary_range: Диапазон зарплат (например: "100000-150000")
    :return: Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    try:
        salary_from, salary_to = map(int, salary_range.split("-"))
    except ValueError:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        # Проверяем, что зарплата указана
        if vacancy.salary["from"] is None and vacancy.salary["to"] is None:
            continue

        # Если указана только нижняя граница
        if vacancy.salary["to"] is None:
            if vacancy.salary["from"] >= salary_from:
                filtered.append(vacancy)
        # Если указана только верхняя граница
        elif vacancy.salary["from"] is None:
            if vacancy.salary["to"] is not None and vacancy.salary["to"] <= salary_to:
                filtered.append(vacancy)
        # Если указаны обе границы
        else:
            if vacancy.salary["from"] >= salary_from and vacancy.salary["to"] <= salary_to:
                filtered.append(vacancy)
    return filtered


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортировка вакансий по зарплате (по убыванию)
    :param vacancies: Список вакансий
    :return: Отсортированный список вакансий
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получение топ N вакансий
    :param vacancies: Список вакансий
    :param top_n: Количество вакансий для вывода
    :return: Список топ N вакансий
    """
    return vacancies[:top_n] if top_n > 0 else vacancies


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Вывод вакансий в консоль
    :param vacancies: Список вакансий для вывода
    """
    if not vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"Вакансия #{i}")
        print(vacancy)
        print("-" * 50)
