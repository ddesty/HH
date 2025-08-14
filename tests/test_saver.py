import json
import os

import pytest

from src.saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def temp_json_file(tmp_path):
    """Фикстура для временного JSON файла"""
    file_path = tmp_path / "test_vacancies.json"
    yield file_path
    if os.path.exists(file_path):
        os.remove(file_path)


def test_json_saver_add_vacancy(temp_json_file) -> None:
    """Тест добавления вакансии в JSON файл"""
    saver = JSONSaver(str(temp_json_file))
    vacancy = Vacancy("Test", "https://example.com", None, "", "")

    saver.add_vacancy(vacancy)

    with open(temp_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["title"] == "Test"


def test_json_saver_read_vacancies(temp_json_file) -> None:
    """Тест чтения вакансий из JSON файла"""
    test_data = [
        {
            "name": "Test",  # Изменено с 'title' на 'name'
            "alternate_url": "https://example.com",  # Изменено с 'url' на 'alternate_url'
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"responsibility": "Test description", "requirement": "Test requirements"},
        }
    ]

    # Записываем данные в файл
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)

    saver = JSONSaver(str(temp_json_file))

    # Проверяем чтение сырых данных
    raw_data = saver._JSONSaver__read_vacancies()
    assert len(raw_data) == 1
    assert raw_data[0]["name"] == "Test"

    # Проверяем преобразование в объекты Vacancy
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1
    assert isinstance(vacancies[0], Vacancy)
    assert vacancies[0].title == "Test"
