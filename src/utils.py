
def select_platform():
    """Функция для выбора платформ"""
    # Предлагаем пользователю выбрать платформы
    print("Выберите платформу для поиска вакансий:")
    # Список доступных платформ и их символы
    platforms = [("hh.ru", "h"), ("superjob.ru", "s")]
    for i, (platform, symbol) in enumerate(platforms):
        print(f"{i + 1}. {platform}")
    # Просим ввести символы платформ, через запятую
    platform_symbols = input("Введите символы платформ через запятую (например: h,s): ")
    # Получаем выбранные платформы
    selected_platforms = []
    for symbol in platform_symbols.split(","):
        for platform, p_symbol in platforms:
            if p_symbol == symbol.strip():
                selected_platforms.append(platform)
    return selected_platforms


def input_query():
    """Функция для ввода поискового запроса"""
    # Просим пользователя ввести поисковой запрос
    query = input("Введите поисковой запрос: ")
    return query


def show_top_vacancies(vacancies, n=10):
    """Функция для отображения топ N вакансий"""
    # Сортируем вакансии по зарплате
    sorted_vacancies = sorted(vacancies, reverse=True)
    # Отображаем top N вакансий
    print(f"Топ {n} вакансий:")
    for i, vacancy in enumerate(sorted_vacancies[:n]):
        print(f"{i + 1}. {vacancy.title} {vacancy.salary} {vacancy.link}")


def show_sorted_vacancies(vacancies):
    """Функция для отображения вакансий в отсортированном виде"""
    # Сортируем вакансии по зарплате
    sorted_vacancies = sorted(vacancies, reverse=True)
    # Отображаем отсортированный список вакансий
    print("Список вакансий:")
    for i, vacancy in enumerate(sorted_vacancies):
        print(f"{i + 1}. {vacancy.title} {vacancy.salary} {vacancy.link}")


def show_filtered_vacancies(vacancies, keyword=None, salary_from=None, salary_to=None):
    """Функция для отображения вакансий по заданным критериям"""
    # Фильтруем вакансии по ключевому слову, если оно задано
    if keyword is not None:
        filtered_vacancies = [v for v in vacancies if keyword.lower() in v.description.lower()]
    else:
        filtered_vacancies = vacancies
    # Фильтруем вакансии по зарплате, если значения указаны
    if salary_from is not None:
        filtered_vacancies = [v for v in filtered_vacancies if v.salary >= salary_from]
    if salary_to is not None:
        filtered_vacancies = [v for v in filtered_vacancies if v.salary <= salary_to]
    # Отображаем отфильтрованный список вакансий
    print("Список вакансий:")
    for i, vacancy in enumerate(filtered_vacancies):
        print(f"{i + 1}. {vacancy.title} {vacancy.salary} {vacancy.link}")


def edit_vacancies(file, action, vacancy=None):
    """Функция для добавления, редактирования и удаления вакансий в файле"""
    # Читаем текущие вакансии из файла
    vacancies = file.read()
    # Обрабатываем команду пользователя
    if action == "add":
        # Добавляем новую вакансию
        if vacancy.validate():
            vacancies.append(vacancy)
            file.write([v.__dict__ for v in vacancies])
            print("Вакансия успешно добавлена!")
        else:
            print("Ошибка! Проверьте правильность введенных данных.")
    elif action == "edit":
        # Изменяем существующую вакансию
        if vacancy.validate():
            for i, v in enumerate(vacancies):
                if v == vacancy:
                    vacancies[i] = vacancy
                    file.write([v.__dict__ for v in vacancies])
                    print("Изменения успешно сохранены!")
                    break
            else:
                print("Ошибка! Не найдено вакансии, которую нужно изменить.")
        else:
            print("Ошибка! Проверьте правильность введенных данных.")
    elif action == "remove":
        # Удаляем существующую вакансию
        for i, v in enumerate(vacancies):
            if v == vacancy:
                vacancies.pop(i)
                file.write([v.__dict__ for v in vacancies])
                print("Вакансия успешно удалена!")
                break
        else:
            print("Ошибка! Не найдено вакансии, которую нужно удалить.")
