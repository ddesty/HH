from src.api import HeadHunterAPI
from src.saver import JSONSaver
from src.utils import filter_vacancies
from src.utils import get_top_vacancies
from src.utils import get_vacancies_by_salary
from src.utils import print_vacancies
from src.utils import sort_vacancies
from src.vacancy import Vacancy


def user_interaction() -> None:
    print("Добро пожаловать в программу для работы с вакансиями с hh.ru!")

    hh_api = HeadHunterAPI()
    search_query = input("Введите поисковый запрос (например: Python): ").strip()
    print("Идет загрузка вакансий...")

    try:
        hh_vacancies = hh_api.get_vacancies(search_query)
        vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
        print(f"Загружено {len(vacancies_list)} вакансий")

        json_saver = JSONSaver()
        for vacancy in vacancies_list:
            json_saver.add_vacancy(vacancy)

        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        filter_words = input("Введите ключевые слова для фильтрации вакансий: ").strip()
        salary_range = input("Введите диапазон зарплат (например: 100000-150000): ").strip()

        filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
        print(f"После фильтрации по ключевым словам осталось {len(filtered_vacancies)} вакансий")

        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
        print(f"После фильтрации по зарплате осталось {len(ranged_vacancies)} вакансий")

        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        print("\nРезультаты поиска:")
        print_vacancies(top_vacancies)

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    user_interaction()
