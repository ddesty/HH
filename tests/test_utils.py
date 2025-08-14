import pytest

from src.utils import filter_vacancies
from src.utils import get_top_vacancies
from src.utils import get_vacancies_by_salary
from src.utils import sort_vacancies
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancies() -> list[Vacancy]:
    """Фикстура с тестовыми вакансиями"""
    return [
        Vacancy(
            "Python Developer",
            "https://example.com/1",
            {"from": 100000, "to": 150000, "currency": "RUR"},
            "Python SQL",
            "Experience with Python",
        ),
        Vacancy(
            "Java Developer",
            "https://example.com/2",
            {"from": 90000, "to": 120000, "currency": "RUR"},
            "Java SQL",
            "Experience with Java",
        ),
        Vacancy(
            "SQL Expert",
            "https://example.com/3",
            {"from": 80000, "to": None, "currency": "RUR"},
            "Advanced SQL",
            "SQL experience",
        ),
    ]


def test_filter_vacancies(sample_vacancies) -> None:
    """Тест фильтрации по ключевому слову"""
    result = filter_vacancies(sample_vacancies, "SQL")
    assert len(result) == 3

    result = filter_vacancies(sample_vacancies, "Python")
    assert len(result) == 1
    assert result[0].title == "Python Developer"


def test_get_vacancies_by_salary(sample_vacancies) -> None:
    """Тест фильтрации по зарплате"""
    result = get_vacancies_by_salary(sample_vacancies, "80000-130000")
    assert len(result) == 2

    result = get_vacancies_by_salary(sample_vacancies, "")
    assert len(result) == 3


def test_sort_vacancies(sample_vacancies) -> None:
    """Тест сортировки вакансий"""
    sorted_vac = sort_vacancies(sample_vacancies)
    assert sorted_vac[0].title == "Python Developer"
    assert sorted_vac[1].title == "Java Developer"
    assert sorted_vac[2].title == "SQL Expert"


def test_get_top_vacancies(sample_vacancies) -> None:
    """Тест получения топ N вакансий"""
    top = get_top_vacancies(sample_vacancies, 2)
    assert len(top) == 2
    assert top[0].title == "Python Developer"
