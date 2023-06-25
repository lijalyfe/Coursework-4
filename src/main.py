from src.json_file import JSONFile
from src.vacancy import Vacancy
from src.utils import select_platform, input_query, show_top_vacancies, show_sorted_vacancies, show_filtered_vacancies, edit_vacancies


def main():
    file_manager = JSONFile()
    # Считываем уже имеющиеся вакансии из файла
    vacancies = file_manager.read()
    # Добавляем новые вакансии
    for item in result:
        vacancy = Vacancy(item['title'], item['salary'], item['url'], platform)
        vacancies.append(vacancy)
    # Сортируем вакансии по заработной плате
    sorted_vacancies = show_sorted_vacancies(vacancies)
    # Фильтруем вакансии по минимальной заработной плате
    filtered_vacancies = show_filtered_vacancies(sorted_vacancies)
    # Редактируем вакансии
    edit_vacancies(filtered_vacancies)
    # Выводим топ-10 вакансий
    show_top_vacancies(filtered_vacancies)

    if __name__ == '__main__':
        main()