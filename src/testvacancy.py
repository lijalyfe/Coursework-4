from typing import List, Dict
import requests
import json

class HeadHunterAPI:
    BASE_URL = "https://api.hh.ru/"

    def __init__(self, **kwargs):
        self.params = {}

        # Параметры запроса можно передавать в конструктор
        if kwargs:
            self.params.update(kwargs)

    def get_vacancies(self, search_query: str) -> List[Dict]:
        url = f"{self.BASE_URL}vacancies"
        params = {
            "text": search_query,
        }
        params.update(self.params)
        response = requests.get(url, params=params)

        # Если статус код не 200, генерируем исключение
        response.raise_for_status()

        return response.json()["items"]

class SuperJobAPI:
    BASE_URL = "https://api.superjob.ru/2.33.0/"

    def __init__(self, app_key: str, **kwargs):
        self.params = {"X-Api-App-Id": app_key}

        if kwargs:
            self.params.update(kwargs)

    def get_vacancies(self, search_query: str) -> List[Dict]:
        url = f"{self.BASE_URL}vacancies/"
        params = {
            "keyword": search_query,
        }
        params.update(self.params)
        response = requests.get(url, params=params)

        response.raise_for_status()

        return response.json()["objects"]

class Vacancy:
    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary = salary
        self.description = description

class SalaryRange:
    def __init__(self, salary_string: str) -> None:
        self.min_salary = None
        self.max_salary = None
        self.currency = None
        self._parse_salary(salary_string)

    def _parse_salary(self, salary_string: str) -> None:
        if not salary_string:
            return

        currency_symbols = ["₽", "USD", "EUR"]
        salary_parts = salary_string.replace(" ", "").split("-")

        for idx, part in enumerate(salary_parts):
            if not part.isdigit():
                for symbol in currency_symbols:
                    if symbol in part:
                        self.currency = symbol
                        salary_parts[idx] = part.replace(symbol, "")

                if not self.currency:
                    self.currency = part

        if len(salary_parts) == 1:
            self.min_salary = self.max_salary = salary_parts[0]
        elif len(salary_parts) == 2:
            self.min_salary, self.max_salary = salary_parts

class JSONSaver:
    def __init__(self, filename: str = "vacancies.json") -> None:
        self.filename = filename

    def _load_vacancies(self) -> List[Dict]:
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        return data

    def _save_vacancies(self, data: List[Dict]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy, overwrite: bool = False) -> None:
        data = self._load_vacancies()

        # Если запись уже существует и не нужно перезаписывать - выходим
        if not overwrite and vacancy.url in [item["url"] for item in data]:
            return

        data.append({
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description,
        })

        self._save_vacancies(data)

    def get_vacancies_by_salary(self, salary_range_str: str) -> List[Dict]:
        data = self._load_vacancies()
        salary_range = SalaryRange(salary_range_str)

        filtered_data = [
            item for item in data if item["salary"] and
            salary_range.min_salary <= SalaryRange(item["salary"]).max_salary and
            SalaryRange(item["salary"]).min_salary <= salary_range.max_salary
        ]

        sorted_data = sorted(filtered_data, key=lambda x: SalaryRange(x["salary"]).max_salary, reverse=True)

        return sorted_data

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        data = self._load_vacancies()

        for idx, item in enumerate(data):
            if item["url"] == vacancy.url:
                del data[idx]
                self._save_vacancies(data)
                return

        raise ValueError("Vacancy not found")

def filter_vacancies(hh_vacancies: List[Dict], sj_vacancies: List[Dict], filter_words: List[str]) -> List[Vacancy]:
    filtered_vacancies = []
    all_vacancies = hh_vacancies + sj_vacancies

    for vacancy in all_vacancies:
        if any(word.lower() in vacancy["name"].lower() or
               (vacancy.get("profession") and word.lower() in vacancy["profession"].lower()) or
               (vacancy.get("snippet") and word.lower() in vacancy["snippet"]["requirement"].lower())):
            filtered_vacancies.append(Vacancy(
                title=vacancy["name"],
                url=vacancy["alternate_url"],
                salary=vacancy["salary"] if vacancy.get("salary") else "",
                description=vacancy["description"] if vacancy.get("description") else "",
            ))

    return filtered_vacancies

def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    return sorted(vacancies, key=lambda x: SalaryRange(x.salary).max_salary, reverse=True)

def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    return vacancies[:top_n]

def print_vacancies(vacancies: List[Vacancy]) -> None:
    if not vacancies:
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    for idx, vacancy in enumerate(vacancies):
        print(f"{idx+1}. {vacancy.title}")
        print(f"   Ссылка: {vacancy.url}")
        print(f"   Зарплата: {vacancy.salary}")
        print(f"   Описание: {vacancy.description}\n")

def user_interaction():
    platforms = ["HeadHunter", "SuperJob"]
    app_key = {'v3.r.137636772.89b8dc4297218a5dcf9c8e6f468e738f0182aae0.5d001ac5ff302dddcf98f5f8de641b4d947f0c4e'}
    hh_api = HeadHunterAPI()
    sj_api = SuperJobAPI(app_key)

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    hh_vacancies = hh_api.get_vacancies(search_query)
    sj_vacancies = sj_api.get_vacancies(search_query)

    filtered_vacancies = filter_vacancies(hh_vacancies, sj_vacancies, filter_words)
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    print_vacancies(top_vacancies)

    save_to_file = input("Сохранить вакансии в файл? (y/n): ")
    if save_to_file.lower() == "y":
        json_saver = JSONSaver()
        for vacancy in filtered_vacancies:
            json_saver.add_vacancy(vacancy)

        print("Вакансии сохранены в файл.")


if __name__ == "__main__":
    user_interaction()