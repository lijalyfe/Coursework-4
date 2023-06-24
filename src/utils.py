
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