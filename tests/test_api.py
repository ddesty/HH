from unittest.mock import Mock
from unittest.mock import patch

import pytest

from src.api import HeadHunterAPI


def test_hh_api_connection_success() -> None:
    """Тест успешного подключения к API HH"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        hh_api = HeadHunterAPI()
        hh_api.connect()  # Не должно вызывать исключений


def test_hh_api_connection_failure() -> None:
    """Тест неудачного подключения к API HH"""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        hh_api = HeadHunterAPI()
        with pytest.raises(ConnectionError):
            hh_api.connect()


def test_get_vacancies() -> None:
    """Тест получения вакансий"""
    with patch("requests.get") as mock_get:
        # Настраиваем mock ответа
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy1",
                    "salary": None,
                    "snippet": {"requirement": None, "responsibility": None},
                }
            ],
            "pages": 1,  # Указываем только 1 страницу
        }
        mock_get.return_value = mock_response

        # Создаем экземпляр API
        hh_api = HeadHunterAPI()

        # Заменяем метод connect на пустую функцию, чтобы избежать реальных запросов
        hh_api.connect = lambda: None

        # Устанавливаем параметры для теста
        hh_api._HeadHunterAPI__params = {
            "text": "",
            "page": 0,
            "per_page": 1,  # Только 1 вакансия на страницу
            "_test_mode": True,  # Добавляем флаг тестового режима
        }

        # Получаем вакансии
        result = hh_api.get_vacancies("Python")

        # Проверяем результат
        assert len(result) == 1
        assert result[0]["name"] == "Python Developer"
        assert mock_get.call_count == 1  # Должен быть только один запрос
