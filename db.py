import sqlite3 as sq

def connect_db():
    conn = sq.connect('baza.db')
    cur = conn.cursor()
    return conn, cur

def create_db():
    conn = sq.connect('baza.db')
    cur = conn.cursor()

    # Создание таблицы AppCategories
    cur.execute("""
        CREATE TABLE IF NOT EXISTS AppCategories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT UNIQUE NOT NULL
        )
    """)

    # Создание таблицы ActionTypes
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ActionTypes (
            type_id INTEGER PRIMARY KEY,
            type_name TEXT UNIQUE NOT NULL
        )
    """)

    # Создание таблицы Devices
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Devices (
            device_id INTEGER PRIMARY KEY,
            manufacturer TEXT NOT NULL,
            model TEXT NOT NULL,
            os_version TEXT NOT NULL
        )
    """)

    # Создание таблицы Applications
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Applications (
            app_id INTEGER PRIMARY KEY,
            app_name TEXT NOT NULL UNIQUE,
            platform TEXT CHECK(platform IN ('iOS', 'Android')) NOT NULL,
            app_version TEXT,
            developer TEXT,
            release_date DATE,
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES AppCategories(category_id) ON DELETE CASCADE
        )
    """)

    # Создание таблицы Users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')) NOT NULL,
            registration_date DATE NOT NULL,
            country TEXT,
            device_id INTEGER NOT NULL,
            FOREIGN KEY (device_id) REFERENCES Devices(device_id) ON DELETE CASCADE
        )
    """)

    # Создание таблицы UserActions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS UserActions (
            action_id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            app_id INTEGER NOT NULL,
            action_type_id INTEGER NOT NULL,
            element_name TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (app_id) REFERENCES Applications(app_id) ON DELETE CASCADE,
            FOREIGN KEY (action_type_id) REFERENCES ActionTypes(type_id) ON DELETE CASCADE
        )
    """)

    # Создание таблицы UserPreferences
    cur.execute("""
        CREATE TABLE IF NOT EXISTS UserPreferences (
            preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            app_id INTEGER NOT NULL,
            note TEXT,
            dark_mode BOOLEAN DEFAULT 0,
            notification_allow BOOLEAN DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (app_id) REFERENCES Applications(app_id) ON DELETE CASCADE
        )
    """)


    conn.commit()
    conn.close()

def insert_test_data():
    conn, cur = connect_db()

    # Заполнение AppCategories
    cur.execute("""
        INSERT OR IGNORE INTO AppCategories (category_id, category_name) VALUES
        (1, 'Социальные сети'),
        (2, 'Банкинг'),
        (3, 'Новости'),
        (4, 'Карты и навигация'),
        (5, 'Такси'),
        (6, 'Доставка еды'),
        (7, 'Госуслуги'),
        (8, 'Образование'),
        (9, 'Медицина'),
        (10, 'Путешествия'),
        (11, 'Игры'),
        (12, 'Музыка'),
        (13, 'Видеостриминг'),
        (14, 'Электронная коммерция'),
        (15, 'Фитнес')
    """)

    # Заполнение ActionTypes
    cur.execute("""
        INSERT OR IGNORE INTO ActionTypes (type_id, type_name) VALUES
        (1, 'Вход в аккаунт'),
        (2, 'Поиск'),
        (3, 'Платеж'),
        (4, 'Просмотр профиля'),
        (5, 'Добавление в корзину'),
        (6, 'Скроллинг'),
        (7, 'Просмотр уведомлений'),
        (8, 'Настройка профиля'),
        (9, 'Просмотр карты'),
        (10, 'Заказ такси'),
        (11, 'Просмотр видео'),
        (12, 'Прослушивание музыки'),
        (13, 'Скачивание файла'),
        (14, 'Оценка приложения'),
        (15, 'Подписка')
    """)

    # Заполнение Devices
    cur.execute("""
        INSERT OR IGNORE INTO Devices (device_id, manufacturer, model, os_version) VALUES
        (1, 'Xiaomi', 'Redmi Note 10', 'Android 12'),
        (2, 'Samsung', 'Galaxy S21', 'Android 13'),
        (3, 'Apple', 'iPhone 13', 'iOS 16'),
        (4, 'Huawei', 'P40 Pro', 'EMUI 12'),
        (5, 'Yandex', 'Yandex Phone', 'Yandex OS 2.0'),
        (6, 'Realme', '8 Pro', 'Android 12'),
        (7, 'Honor', '50 Lite', 'Android 13'),
        (8, 'Google', 'Pixel 6', 'Android 14'),
        (9, 'Nokia', 'G21', 'Android 12'),
        (10, 'Inoi', 'A72', 'Android 11'),
        (11, 'Tecno', 'Camon 18', 'Android 12'),
        (12, 'ZTE', 'Blade V40', 'Android 13'),
        (13, 'Vivo', 'Y55', 'Android 12'),
        (14, 'OPPO', 'A76', 'Android 13'),
        (15, 'Motorola', 'Moto G100', 'Android 12')
    """)

    # Заполнение Applications
    cur.execute("""
        INSERT OR IGNORE INTO Applications (app_id, app_name, platform, app_version, developer, release_date, category_id) VALUES
        (1, 'ВКонтакте', 'Android', '5.24', 'VK Team', '2023-01-15', 1),
        (2, 'СберБанк Онлайн', 'iOS', '12.7.1', 'Сбербанк', '2022-11-30', 2),
        (3, 'Яндекс.Карты', 'Android', '4.12', 'Яндекс', '2023-03-22', 4),
        (4, 'Яндекс.Такси', 'iOS', '5.8.3', 'Яндекс', '2023-04-10', 5),
        (5, 'Delivery Club', 'Android', '6.1.0', 'Mail.ru Group', '2023-05-01', 6),
        (6, 'Госуслуги', 'Android', '3.14', 'Минцифры РФ', '2023-02-28', 7),
        (7, 'Учи.ру', 'iOS', '2.5.1', 'Учи.ру', '2023-06-15', 8),
        (8, 'СберЗдоровье', 'Android', '1.9.4', 'Сбербанк', '2023-07-01', 9),
        (9, 'Ostrovok', 'iOS', '4.3.2', 'Ostrovok.ru', '2023-08-12', 10),
        (10, 'World of Tanks Blitz', 'Android', '8.0', 'Lesta Games', '2023-09-20', 11),
        (11, 'Яндекс.Музыка', 'iOS', '5.1.0', 'Яндекс', '2023-10-05', 12),
        (12, 'Кинопоиск', 'Android', '7.2.3', 'Яндекс', '2023-11-11', 13),
        (13, 'Wildberries', 'iOS', '6.9.0', 'Wildberries', '2023-12-01', 14),
        (14, 'FitPrime', 'Android', '2.1.7', 'Сбербанк', '2024-01-15', 15),
        (15, 'Тинькофф', 'iOS', '4.5.6', 'Тинькофф Банк', '2024-02-20', 2)
    """)

    # Заполнение Users
    cur.execute("""
        INSERT OR IGNORE INTO Users (user_id, email, first_name, last_name, age, gender, registration_date, country, device_id) VALUES
        (1, 'ivan.petrov@mail.ru', 'Иван', 'Петров', 28, 'Male', '2023-03-15', 'Россия', 3),
        (2, 'anna.smirnova@gmail.com', 'Анна', 'Смирнова', 34, 'Female', '2023-04-02', 'Россия', 5),
        (3, 'alexey.ivanov@yandex.ru', 'Алексей', 'Иванов', 19, 'Male', '2023-05-20', 'Россия', 2),
        (4, 'ekaterina.sidorova@mail.ru', 'Екатерина', 'Сидорова', 45, 'Female', '2023-06-11', 'Россия', 8),
        (5, 'dmitry.volkov@gmail.com', 'Дмитрий', 'Волков', 22, 'Male', '2023-07-01', 'Россия', 1),
        (6, 'olga.kuznetsova@yandex.ru', 'Ольга', 'Кузнецова', 31, 'Female', '2023-08-19', 'Россия', 10),
        (7, 'sergey.novikov@mail.ru', 'Сергей', 'Новиков', 27, 'Male', '2023-09-25', 'Россия', 4),
        (8, 'marina.fedorova@gmail.com', 'Марина', 'Федорова', 38, 'Female', '2023-10-10', 'Россия', 6),
        (9, 'pavel.morozov@yandex.ru', 'Павел', 'Морозов', 29, 'Male', '2023-11-05', 'Россия', 7),
        (10, 'tatyana.orlova@mail.ru', 'Татьяна', 'Орлова', 41, 'Female', '2023-12-12', 'Россия', 9),
        (11, 'artem.egorov@gmail.com', 'Артем', 'Егоров', 24, 'Male', '2024-01-07', 'Россия', 12),
        (12, 'natalia.vasilieva@yandex.ru', 'Наталия', 'Васильева', 33, 'Female', '2024-02-14', 'Россия', 11),
        (13, 'maxim.belov@mail.ru', 'Максим', 'Белов', 26, 'Male', '2024-03-22', 'Россия', 13),
        (14, 'elena.petrova@gmail.com', 'Елена', 'Петрова', 50, 'Female', '2024-04-30', 'Россия', 14),
        (15, 'vladimir.sokolov@yandex.ru', 'Владимир', 'Соколов', 36, 'Male', '2024-05-18', 'Россия', 15)
    """)

    # Заполнение UserActions
    cur.execute("""
        INSERT OR IGNORE INTO UserActions (action_id, user_id, app_id, action_type_id, element_name) VALUES
        (1, 1, 2, 3, 'Оплата ЖКХ'),
        (2, 2, 4, 10, 'Заказ эконом'),
        (3, 3, 1, 1, 'Кнопка "Войти"'),
        (4, 4, 6, 7, 'Проверка штрафа'),
        (5, 5, 10, 14, 'Оценка 5 звезд'),
        (6, 6, 5, 5, 'Добавление пиццы'),
        (7, 7, 3, 9, 'Построение маршрута'),
        (8, 8, 8, 8, 'Изменение аватарки'),
        (9, 9, 7, 6, 'Прокрутка ленты'),
        (10, 10, 9, 3, 'Оплата отеля'),
        (11, 11, 11, 12, 'Плейлист "Хиты"'),
        (12, 12, 13, 5, 'Добавление платья'),
        (13, 13, 12, 11, 'Просмотр фильма'),
        (14, 14, 14, 15, 'Подписка Premium'),
        (15, 15, 15, 3, 'Перевод средств')
    """)

    # Заполнение UserPreferences
    cur.execute("""
        INSERT OR IGNORE INTO UserPreferences (preference_id, user_id, app_id, note, dark_mode, notification_allow) VALUES
        (1, 1, 2, 'Основной банк', 1, 1),
        (2, 2, 4, 'Рабочие поездки', 0, 1),
        (3, 3, 1, 'Личные сообщения', 1, 0),
        (4, 4, 6, 'Паспортные данные', 1, 1),
        (5, 5, 10, 'Играю вечером', 0, 0),
        (6, 6, 5, 'Любимый ресторан', 1, 1),
        (7, 7, 3, 'Дом и работа', 0, 1),
        (8, 8, 8, 'Медкарта', 1, 0),
        (9, 9, 7, 'Учебные курсы', 1, 1),
        (10, 10, 9, 'Отпуск 2024', 0, 1),
        (11, 11, 11, 'Тренировочная музыка', 1, 1),
        (12, 12, 13, 'Отслеживание заказов', 0, 0),
        (13, 13, 12, 'Избранные фильмы', 1, 1),
        (14, 14, 14, 'Утренние тренировки', 1, 1),
        (15, 15, 15, 'Инвестиции', 0, 1)
    """)
    # -------------------------------cr_userauth----------------------------------
    cur.execute('''
    CREATE TABLE IF NOT EXISTS UserAuth (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('оператор', 'админ'))
    )''')
    # -------------------------------cr_userauth----------------------------------

    conn.commit()
    conn.close()
    


def get_table_info(table_name):
    """
    Универсальная функция для получения информации о таблице:
    - названия столбцов
    - все данные таблицы
    
    Args:
        table_name (str): Название таблицы
        
    Returns:
        dict: Словарь, содержащий:
            - 'columns': список названий столбцов
            - 'data': список кортежей с данными строк
            - 'primary_key': название первичного ключа (если определен)
    """
    conn, cur = connect_db()
    
    # Получение информации о столбцах
    cur.execute(f"PRAGMA table_info({table_name})")
    columns_info = cur.fetchall()
    
    # Извлечение названий столбцов и определение первичного ключа
    columns = []
    primary_key = None
    
    for col_info in columns_info:
        col_name = col_info[1]
        is_pk = col_info[5]  # 5-й элемент содержит флаг первичного ключа (1 = PK)
        
        columns.append(col_name)
        if is_pk == 1:
            primary_key = col_name
    
    # Получение всех данных из таблицы
    cur.execute(f"SELECT * FROM {table_name}")
    data = cur.fetchall()
    
    conn.close()
    
    return {
        'columns': columns,
        'data': data,
        'primary_key': primary_key
    }


def add_record(table_name, record_data):
    """
    Универсальная функция для добавления записи в таблицу
    
    Args:
        table_name (str): Название таблицы
        record_data (dict): Словарь {название_столбца: значение}
        
    Returns:
        int: ID добавленной записи (если есть)
        
    Raises:
        ValueError: Если параметры не корректны
        Exception: В случае ошибки при добавлении записи
    """
    if not table_name:
        raise ValueError("Не указано название таблицы")
    
    if not record_data or not isinstance(record_data, dict):
        raise ValueError("Данные для записи должны быть переданы в виде словаря")
    
    if len(record_data) == 0:
        raise ValueError("Не указаны данные для добавления")
        
    conn, cur = connect_db()
    
    # Формирование SQL запроса
    columns = ', '.join(record_data.keys())
    placeholders = ', '.join(['?' for _ in record_data])
    values = list(record_data.values())
    
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    
    try:
        # Проверка наличия таблицы
        cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cur.fetchone():
            raise ValueError(f"Таблица '{table_name}' не существует в базе данных")
            
        # Выполнение запроса
        cur.execute(query, values)
        
        # Получение ID последней вставленной записи
        last_id = cur.lastrowid
        
        conn.commit()
        return last_id
    except Exception as e:
        error_message = str(e)
        print(f"Ошибка при добавлении записи: {error_message}")
        conn.rollback()
        
        # Улучшенная обработка ошибок UNIQUE constraint
        if "UNIQUE constraint failed" in error_message:
            constraint_field = error_message.split("failed: ")[1].split(".")[1] if "failed: " in error_message else "unknown"
            raise ValueError(f"Запись с таким значением поля '{constraint_field}' уже существует")
        else:
            # Пробрасываем исключение дальше для обработки в UI
            raise
    finally:
        conn.close()


def delete_record(table_name, conditions):
    """
    Универсальная функция для удаления записей из таблицы
    
    Args:
        table_name (str): Название таблицы
        conditions (dict): Словарь условий {название_столбца: значение}
            Если значение - кортеж из (оператор, значение), используется указанный оператор
            Пример: {'user_id': 5} - удалит записи где user_id = 5
                   {'age': ('>', 18)} - удалит записи где age > 18
    
    Returns:
        int: Количество удаленных записей или None в случае ошибки
        
    Raises:
        ValueError: Если параметры не корректны
        RuntimeError: В случае ошибки при удалении записи
    """
    if not table_name:
        raise ValueError("Не указано название таблицы")
    
    conn, cur = connect_db()
    
    try:
        # Проверка существования таблицы
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if not cur.fetchone():
            raise ValueError(f"Таблица '{table_name}' не существует в базе данных")
            
        if not conditions:
            raise ValueError("Необходимо указать условия для удаления записей")
        
        # Формирование условий WHERE
        where_clauses = []
        values = []
        
        for column, condition in conditions.items():
            if isinstance(condition, tuple) and len(condition) == 2:
                operator, value = condition
                where_clauses.append(f"{column} {operator} ?")
                values.append(value)
            else:
                where_clauses.append(f"{column} = ?")
                values.append(condition)
        
        # Формирование SQL запроса
        query = f"DELETE FROM {table_name}"
        if where_clauses:
            query += f" WHERE {' AND '.join(where_clauses)}"
        
        # Выполнение запроса
        cur.execute(query, values)
        
        # Получение количества удаленных строк
        deleted_count = cur.rowcount
        
        conn.commit()
        return deleted_count
    except Exception as e:
        error_message = str(e)
        print(f"Ошибка при удалении записей: {error_message}")
        conn.rollback()
        
        if "no such table" in error_message:
            raise ValueError(f"Таблица '{table_name}' не существует в базе данных")
        elif "no such column" in error_message:
            column_name = error_message.split("no such column: ")[1].split(" ")[0] if "no such column: " in error_message else "unknown"
            raise ValueError(f"Столбец '{column_name}' не существует в таблице '{table_name}'")
        else:
            raise RuntimeError(f"Ошибка при удалении записей: {error_message}")
    finally:
        conn.close()


create_db()
insert_test_data()