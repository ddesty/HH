import pytest

from src.vacancy import Vacancy


def test_vacancy_creation() -> None:
    """Тест создания вакансии"""
    vacancy = Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Разработка на Python",
        requirements="Опыт работы от 3 лет",
    )
    assert vacancy.title == "Python Developer"
    assert vacancy.salary["from"] == 100000
    assert vacancy.url.startswith("http")


def test_vacancy_comparison() -> None:
    """Тест сравнения вакансий"""
    v1 = Vacancy("Dev1", "https://example.com/1", {"from": 100000, "to": 150000, "currency": "RUR"}, "", "")
    v2 = Vacancy("Dev2", "https://example.com/2", {"from": 120000, "to": 180000, "currency": "RUR"}, "", "")

    assert v2 > v1
    assert v1 < v2
    assert v1 != v2


def test_vacancy_str() -> None:
    """Тест строкового представления"""
    vacancy = Vacancy("Dev", "https://example.com", None, "Desc", "Req")
    assert "Dev" in str(vacancy)
    assert "не указана" in str(vacancy)
