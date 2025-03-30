import flet as ft
from flet import ThemeMode, Icons, BorderSide, ButtonStyle, RoundedRectangleBorder
import db

# класс для хранения данных сессии
class Session:
    def __init__(self):
        self.username = ""
        self.role = ""
        self.is_authenticated = False

#создаем глобальный объект сессии
session = Session()

# Функция для показа SnackBar с сообщением об ошибке
def show_error_snackbar(page, message):
    page.open(ft.SnackBar(
        content=ft.Text(message, weight=ft.FontWeight.W_500),
        bgcolor="#F44336",  # Красный цвет для ошибок
        action="Закрыть",
        action_color="white",
    ))
    page.update()

# Функция для показа SnackBar с сообщением об успехе
def show_success_snackbar(page, message):
    page.open(ft.SnackBar(
        content=ft.Text(message, weight=ft.FontWeight.W_500),
        bgcolor="#4CAF50",  # Зеленый цвет для успешных операций
        action="Закрыть",
        action_color="white",
    ))
    page.update()

def exit_app(e):
    page = e.page
    
    def handle_close(e):
        if e.control.text == "Да":
            page.window.close()
        page.close(confirm_dialog)

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Подтверждение", weight=ft.FontWeight.BOLD),
        content=ft.Text("Вы уверены, что хотите выйти?"),
        actions=[
            ft.TextButton("Нет", on_click=handle_close),
            ft.TextButton("Да", on_click=handle_close, style=ButtonStyle(color="red")),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.open(confirm_dialog)

def go_to_login(e):
    page = e.page
    page.controls.clear()
    login_page(page)
    page.update()

def go_to_register(e):
    page = e.page
    page.controls.clear()
    register_page(page)
    page.update()

def login_page(page: ft.Page):
    page.title = "Авторизация"
    page.theme_mode = ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1500
    page.window.height = 900
    page.window.resizable = True
    page.window.center()
   
    #создаем поля ввода и кнопку
    auth_username = ft.TextField(
        label="Логин",
        width=300,
        text_size=16,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        prefix_icon=Icons.PERSON,
    )
    
    auth_password = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        width=300,
        text_size=16,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        prefix_icon=Icons.LOCK,
    )
    
    auth_button = ft.FilledButton(
        text="Вход",
        width=300, 
        disabled=True,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
        icon=Icons.LOGIN
    )
    
    go_to_register_button = ft.OutlinedButton(
        text="Регистрация",
        width=300,
        on_click=go_to_register,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
        icon=Icons.PERSON_ADD
    )
    
    login_status = ft.Text(" ", size=16, weight=ft.FontWeight.W_500)

    #функция для проверки заполнения полей
    def validate(e):
        if all([auth_username.value, auth_password.value]):
            auth_button.disabled = False
        else:
            auth_button.disabled = True
        page.update()
    
    #привязываем обработчик к полям ввода
    auth_username.on_change = validate
    auth_password.on_change = validate

    def login_click(e):
        username = auth_username.value
        password = auth_password.value
        
        if not username or not password:
            login_status.value = "Заполните все поля!"
            login_status.color = "red"
            page.update()
            return
        
        #получаем информацию о таблице UserAuth
        user_auth_info = db.get_table_info("UserAuth")
        
        #поиск пользователя по имени и паролю
        user = None
        for row in user_auth_info['data']:
            if row[1] == username and row[2] == password:  #индекс 1 - username, 2 - password
                user = row
                break
        
        if user:
            #успешная авторизация
            login_status.value = "Успешная авторизация!"
            login_status.color = "green"
            page.update()
            
            #сохраняем данные в сессии
            session.username = user[1]  #имя пользователя
            session.role = user[3]      #роль пользователя
            session.is_authenticated = True
            
            #переходим на главную страницу
            page.controls.clear()
            page.add(hello_user_page(page))
            page.update()
        else:
            login_status.value = "Неверный логин или пароль!"
            login_status.color = "red"
            page.update()
    
    #привязываем функцию к кнопке
    auth_button.on_click = login_click

    page.add(
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Вход в управление", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=20, color="transparent"),
                        auth_username,
                        auth_password,
                        ft.Divider(height=10, color="transparent"),
                        auth_button,
                        go_to_register_button,
                        login_status,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=30,
                width=400,
            ),
            elevation=5,
            surface_tint_color="#E0E0E0",
        )
    )
    
    page.add(
        ft.Container(
            content=ft.FilledTonalButton(
                text="Выход", 
                width=300, 
                on_click=exit_app,
                icon=Icons.EXIT_TO_APP,
                style=ButtonStyle(
                    shape=RoundedRectangleBorder(radius=8),
                ),
            ),
            alignment=ft.alignment.bottom_center,
            margin=20,
        )
    )
    
def register_page(page: ft.Page):
    page.title = "Регистрация"
    page.theme_mode = ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1500
    page.window.height = 900

    reg_status = ft.Text(" ", size=16, weight=ft.FontWeight.W_500)
    
    reg_username = ft.TextField(
        label="Логин",
        width=300,
        text_size=16,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        prefix_icon=Icons.PERSON,
    )
    
    reg_password = ft.TextField(
        label="Пароль",
        password=True,
        can_reveal_password=True,
        width=300,
        text_size=16,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        prefix_icon=Icons.LOCK,
    )
    
    reg_role_dropdown = ft.Dropdown(
        label="Выберите роль",
        options=[
            ft.dropdown.Option("operator", text="Оператор"),
            ft.dropdown.Option("admin", text="Админ"),
        ],
        width=300,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
    )
    
    reg_button = ft.FilledButton(
        text="Зарегистрироваться",
        width=300,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
        icon=Icons.PERSON_ADD,
    )
    
    go_to_login_button = ft.OutlinedButton(
        text="Назад",
        width=300,
        on_click=go_to_login,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
        icon=Icons.ARROW_BACK,
    )

    def register_click(e):
        #получаем значения из полей ввода
        username = reg_username.value
        password = reg_password.value
        role = reg_role_dropdown.value
        
        #проверка на пустые поля
        if not username or not password or not role:
            reg_status.value = "Заполните все поля!"
            reg_status.color = "red"
            page.update()
            return
        
        #подготовка данных для добавления
        user_data = {
            "username": username,
            "password": password,
            "role": "оператор" if role == "operator" else "админ"
        }
        
        #добавление пользователя в базу данных
        try:
            user_id = db.add_record("UserAuth", user_data)
            if user_id:
                reg_status.value = "Регистрация успешна!"
                reg_status.color = "green"
                #очистка полей
                reg_username.value = ""
                reg_password.value = ""
                reg_role_dropdown.value = None
                show_success_snackbar(page, "Пользователь успешно зарегистрирован")
            else:
                reg_status.value = "Ошибка при регистрации. Возможно, пользователь уже существует."
                reg_status.color = "red"
                show_error_snackbar(page, "Не удалось зарегистрировать пользователя")
        except Exception as e:
            error_msg = str(e)
            if "UNIQUE constraint failed" in error_msg:
                reg_status.value = "Пользователь с таким логином уже существует"
                show_error_snackbar(page, "Пользователь с таким логином уже существует")
            else:
                reg_status.value = f"Ошибка: {error_msg}"
                show_error_snackbar(page, f"Ошибка базы данных: {error_msg}")
            reg_status.color = "red"
        
        page.update()
    
    #привязываем функцию к кнопке
    reg_button.on_click = register_click

    page.add(
        ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Регистрация", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ft.Divider(height=20, color="transparent"),
                        reg_username,
                        reg_password,
                        reg_role_dropdown,
                        ft.Divider(height=10, color="transparent"),
                        reg_button,
                        reg_status,
                        go_to_login_button,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=30,
                width=400,
            ),
            elevation=5,
            surface_tint_color="#E0E0E0",
        )
    )


def hello_user_page(page: ft.Page):
    page.title = "Управление данными"
    page.theme_mode = ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 1500
    page.window.height = 900
    
    def logout_clicked(e):
        session.is_authenticated = False
        session.username = ""
        session.role = ""
        go_to_login(e)
    
    def show_admin_panel(e):
        page.controls.clear()
        page.add(admin_panel_view(page))
        page.update()
        
    def show_admin_tables_panel(e):
        page.controls.clear()
        page.add(admin_tables_view(page))
        page.update()
    
    def show_operator_panel(e):
        page.controls.clear()
        page.add(operator_panel_view(page))
        page.update()
    
    #основной контент страницы
    title = ft.Text(
        f"Добро пожаловать, {session.username}!", 
        size=30, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    role_info = ft.Text(
        f"Роль: {session.role}", 
        size=16, 
        weight=ft.FontWeight.W_500,
        text_align=ft.TextAlign.CENTER
    )    
    
    logout_button = ft.FilledTonalButton(
        "Выйти из системы", 
        width=300, 
        on_click=logout_clicked,
        icon=Icons.LOGOUT,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
    )
    
    #здесь добавляется основной функционал в зависимости от роли пользователя
    if session.role == "админ":
        role_specific_content = ft.Text(
            "Панель администратора", 
            size=20,
            weight=ft.FontWeight.W_500
        )
        
        #кнопки для перехода к управлению пользователями и таблицами
        admin_button = ft.FilledButton(
            "Управление пользователями", 
            width=300, 
            on_click=show_admin_panel,
            icon=Icons.MANAGE_ACCOUNTS,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=8),
            ),
        )
        
        tables_button = ft.FilledButton(
            "Просмотр таблиц", 
            width=300, 
            on_click=show_admin_tables_panel,
            icon=Icons.TABLE_CHART,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=8),
            ),
        )
        
        admin_content = ft.Column([
            role_specific_content, 
            admin_button,
            tables_button
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        
        role_specific_content = admin_content
    else:
        role_specific_content = ft.Column([
            ft.Text(
                "Панель оператора", 
                size=20,
                weight=ft.FontWeight.W_500
            ), 
            ft.FilledButton(
                "Управление данными", 
                width=300, 
                on_click=show_operator_panel,
                icon=Icons.EDIT_NOTE,
                style=ButtonStyle(
                    shape=RoundedRectangleBorder(radius=8),
                ),
            )
        ])

    content = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    title,
                    role_info,
                    ft.Divider(height=30, color="transparent"),
                    role_specific_content,
                    ft.Divider(height=30, color="transparent"),
                    logout_button
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            ),
            padding=40,
            width=500,
        ),
        elevation=5,
        surface_tint_color="#E0E0E0",
    )
    
    return content


#функция для проверки прав доступа
def check_permission(required_role):
    return session.is_authenticated and session.role == required_role

#функция для удаления записи из таблицы
def delete_record(table_name, record_id):
    """
    Удаляет запись из таблицы по её ID
    
    Args:
        table_name (str): Название таблицы
        record_id (int): ID записи для удаления
        
    Returns:
        bool: True если удаление прошло успешно, иначе False
    """
    conn, cur = db.connect_db()
    
    try:
        # Получение информации о первичном ключе таблицы
        table_info = db.get_table_info(table_name)
        primary_key = table_info['primary_key']
        
        if not primary_key:
            print(f"Не удалось найти первичный ключ для таблицы {table_name}")
            return False
        
        # Выполнение запроса на удаление
        cur.execute(f"DELETE FROM {table_name} WHERE {primary_key} = ?", (record_id,))
        conn.commit()
        
        # Проверка, была ли удалена запись
        if cur.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при удалении записи: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

#функция для обновления данных пользователя
def update_user(user_id, username, password=None, role=None):
    """
    Обновляет данные пользователя
    
    Args:
        user_id (int): ID пользователя для обновления
        username (str): Новое имя пользователя
        password (str, optional): Новый пароль. Если None, пароль не меняется
        role (str, optional): Новая роль. Если None, роль не меняется
        
    Returns:
        bool: True если обновление прошло успешно, иначе False
        
    Raises:
        Exception: При ошибке выполнения запроса или проблемах с базой данных
    """
    conn, cur = db.connect_db()
    
    try:
        #получение текущих данных пользователя
        user_info = db.get_table_info("UserAuth")
        
        user = None
        for row in user_info['data']:
            if row[0] == user_id:
                user = row
                break
        
        if not user:
            print(f"Пользователь с ID {user_id} не найден")
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        #формирование запроса в зависимости от предоставленных данных
        query_parts = []
        params = []
        
        if username:
            # Проверка на уникальность имени пользователя
            for row in user_info['data']:
                if row[1] == username and row[0] != user_id:
                    raise ValueError(f"Пользователь с логином '{username}' уже существует")
            
            query_parts.append("username = ?")
            params.append(username)
        
        if password:
            query_parts.append("password = ?")
            params.append(password)
        
        if role:
            query_parts.append("role = ?")
            params.append(role)
        
        if not query_parts:
            #нечего обновлять
            return True
        
        query = f"UPDATE UserAuth SET {', '.join(query_parts)} WHERE id = ?"
        params.append(user_id)
        
        #выполнение запроса
        cur.execute(query, params)
        conn.commit()
        
        return True
    except Exception as e:
        print(f"Ошибка при обновлении пользователя: {e}")
        conn.rollback()
        raise  # Пробрасываем исключение дальше для обработки в UI
    finally:
        conn.close()


def admin_panel_view(page):
    def show_main_screen():
        page.controls.clear()
        page.add(hello_user_page(page))
        page.update()
    
    if not check_permission('админ'):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "У вас нет прав для доступа к этой панели", 
                        size=20, 
                        color="red",
                        weight=ft.FontWeight.W_500
                    ),
                    ft.FilledButton(
                        "Вернуться на главный экран",
                        on_click=lambda e: show_main_screen(),
                        icon=Icons.HOME,
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=8),
                        ),
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=30,
            ),
            elevation=5,
        )
    
    title = ft.Text(
        "Управление пользователями", 
        size=28, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    #создание таблицы пользователей
    users_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Логин", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Роль", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Действия", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, "#BDBDBD"),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, "#E0E0E0"),
        horizontal_lines=ft.border.BorderSide(1, "#E0E0E0"),
        sort_column_index=0,
        heading_row_height=50,
        data_row_min_height=50,
    )
    
    #функция для обновления таблицы пользователей
    def update_users_table():
        #получаем информацию о пользователях с помощью get_table_info
        user_info = db.get_table_info("UserAuth")
        users_table.rows.clear()
        
        for user in user_info['data']:
            edit_button = ft.IconButton(
                icon=Icons.EDIT,
                tooltip="Редактировать",
                on_click=lambda e, user_id=user[0]: edit_user_dialog(user_id)
            )
            
            delete_button = ft.IconButton(
                icon=Icons.DELETE,
                tooltip="Удалить",
                on_click=lambda e, user_id=user[0]: delete_user(user_id)
            )
            
            actions = ft.Row([edit_button, delete_button])
            
            users_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(user[0]))),  # ID
                        ft.DataCell(ft.Text(user[1])),       # Логин (username)
                        ft.DataCell(ft.Text(user[3])),       # Роль (индекс 3)
                        ft.DataCell(actions),
                    ]
                )
            )
        page.update()
    
    #функция для удаления пользователя
    def delete_user(user_id):
        def confirm_delete(e):
            try:
                #используем функцию delete_record из db.py
                deleted_count = db.delete_record("UserAuth", {"id": user_id})
                
                if deleted_count and deleted_count > 0:
                    page.close(delete_dialog)
                    update_users_table()
                    show_success_snackbar(page, "Пользователь успешно удален")
                else:
                    page.close(delete_dialog)
                    show_error_snackbar(page, "Не удалось удалить пользователя")
            except Exception as e:
                page.close(delete_dialog)
                show_error_snackbar(page, f"Ошибка при удалении: {str(e)}")
        
        #диалог подтверждения удаления
        delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text("Вы уверены, что хотите удалить этого пользователя?"),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: page.close(delete_dialog)),
                ft.TextButton("Удалить", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(delete_dialog)
    
    #функция получения пользователя по ID
    def get_user_by_id(user_id):
        user_info = db.get_table_info("UserAuth")
        for user in user_info['data']:
            if user[0] == user_id:
                return user
        return None
    
    #функция для обновления пользователя
    def update_user(user_id, username, password=None, role=None):
        #получаем соединение с БД
        conn, cur = db.connect_db()
        
        try:
            if password:
                #если указан новый пароль, обновляем все поля
                cur.execute(
                    "UPDATE UserAuth SET username = ?, password = ?, role = ? WHERE id = ?",
                    (username, password, role, user_id)
                )
            else:
                #если пароль не указан, не меняем его
                cur.execute(
                    "UPDATE UserAuth SET username = ?, role = ? WHERE id = ?",
                    (username, role, user_id)
                )
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка при обновлении пользователя: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    #функция для проверки существования пользователя
    def check_user_exists(username):
        user_info = db.get_table_info("UserAuth")
        for user in user_info['data']:
            if user[1] == username:
                return True
        return False
    
    #функция для показа диалога редактирования пользователя
    def edit_user_dialog(user_id):
        #получаем данные пользователя по ID
        user = get_user_by_id(user_id)
        
        if not user:
            print(f"Пользователь с ID {user_id} не найден")
            return
        
        edit_username_input = ft.TextField(
            label="Логин",
            value=user[1],
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            width=300,
            prefix_icon=Icons.PERSON
        )
        
        edit_password_input = ft.TextField(
            label="Новый пароль (оставьте пустым, чтобы не менять)",
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            width=300,
            password=True,
            can_reveal_password=True,
            prefix_icon=Icons.LOCK
        )
        
        edit_role_dropdown = ft.Dropdown(
            label="Роль",
            width=300,
            options=[
                ft.dropdown.Option("оператор", text="Оператор"),
                ft.dropdown.Option("админ", text="Администратор")
            ],
            value=user[3],
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
        )
        
        edit_status_text = ft.Text(
            "",
            size=16,
            color="red",
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500
        )
        
        #функция сохранения изменений
        def save_edited_user(e):
            new_username = edit_username_input.value
            new_password = edit_password_input.value
            new_role = edit_role_dropdown.value
            
            if not new_username or not new_role:
                edit_status_text.value = "Имя пользователя и роль не могут быть пустыми"
                edit_status_text.color = "red"
                page.update()
                return
            
            try:
                if update_user(user_id, new_username, new_password, new_role):
                    page.close(edit_dialog)
                    update_users_table()
                    show_success_snackbar(page, "Данные пользователя успешно обновлены")
            except Exception as e:
                error_msg = str(e)
                if "уже существует" in error_msg:
                    edit_status_text.value = "Пользователь с таким логином уже существует"
                    show_error_snackbar(page, "Пользователь с таким логином уже существует")
                else:
                    edit_status_text.value = f"Ошибка: {error_msg}"
                    show_error_snackbar(page, f"Ошибка при обновлении: {error_msg}")
                edit_status_text.color = "red"
                page.update()
        
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование пользователя"),
            content=ft.Column([
                edit_username_input,
                edit_password_input,
                edit_role_dropdown,
                edit_status_text
            ], width=300, height=250, spacing=10),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: page.close(edit_dialog)),
                ft.FilledButton(
                    "Сохранить", 
                    on_click=save_edited_user,
                    icon=Icons.SAVE,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(edit_dialog)
    
    #функция для показа диалога добавления пользователя
    def add_user_dialog(e):
        add_username_input = ft.TextField(
            label="Логин",
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            width=300,
            prefix_icon=Icons.PERSON
        )
        
        add_password_input = ft.TextField(
            label="Пароль",
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
            width=300,
            password=True,
            can_reveal_password=True,
            prefix_icon=Icons.LOCK
        )
        
        add_role_dropdown = ft.Dropdown(
            label="Роль",
            width=300,
            options=[
                ft.dropdown.Option("оператор", text="Оператор"),
                ft.dropdown.Option("админ", text="Администратор")
            ],
            border=ft.InputBorder.OUTLINE,
            border_radius=8,
        )
        
        add_status_text = ft.Text(
            "",
            size=16,
            color="red",
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500
        )
        
        def save_new_user(e):
            username = add_username_input.value
            password = add_password_input.value
            role = add_role_dropdown.value
            
            if not username or not password or not role:
                add_status_text.value = "Заполните все поля"
                add_status_text.color = "red"
                page.update()
                return
            
            #проверка существования пользователя
            if check_user_exists(username):
                add_status_text.value = "Пользователь с таким логином уже существует"
                add_status_text.color = "red"
                page.update()
                show_error_snackbar(page, "Пользователь с таким логином уже существует")
                return
            
            #добавление нового пользователя
            user_data = {
                "username": username,
                "password": password,
                "role": role
            }
            
            try:
                db.add_record("UserAuth", user_data)
                page.close(add_dialog)
                update_users_table()
                show_success_snackbar(page, "Пользователь успешно добавлен")
            except Exception as e:
                error_msg = str(e)
                if "UNIQUE constraint failed" in error_msg:
                    add_status_text.value = "Пользователь с таким логином уже существует"
                    show_error_snackbar(page, "Пользователь с таким логином уже существует")
                else:
                    add_status_text.value = f"Ошибка: {error_msg}"
                    show_error_snackbar(page, f"Ошибка базы данных: {error_msg}")
                add_status_text.color = "red"
                page.update()
        
        add_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Добавление нового пользователя"),
            content=ft.Column([
                add_username_input,
                add_password_input,
                add_role_dropdown,
                add_status_text
            ], width=300, height=250, spacing=10),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: page.close(add_dialog)),
                ft.TextButton("Сохранить", on_click=save_new_user),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(add_dialog)
    
    #кнопка для добавления нового пользователя
    add_button = ft.FilledButton(
        "Добавить пользователя",
        on_click=add_user_dialog,
        icon=Icons.PERSON_ADD,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
    )
    
    #кнопка для возврата на главный экран
    back_button = ft.FilledTonalButton(
        "Вернуться на главный экран",
        on_click=lambda e: show_main_screen(),
        icon=Icons.HOME,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
    )
    
    #первоначальное заполнение таблицы
    update_users_table()
    
    #сборка интерфейса
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                title,
                ft.Divider(height=10, color="transparent"),
                users_table,
                ft.Divider(height=10, color="transparent"),
                ft.Row([add_button], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=10, color="transparent"),
                ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            padding=30,
            expand=True,
        ),
        elevation=5,
        surface_tint_color="#E0E0E0",
        margin=20,
    )

def operator_panel_view(page):
    #проверка прав доступа
    def check_permission():
        return session.is_authenticated and session.role == "оператор"
        
    def show_main_screen():
        page.controls.clear()
        page.add(hello_user_page(page))
        page.update()
    
    if not check_permission():
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "У вас нет прав для доступа к этой панели", 
                        size=20, 
                        color="red",
                        weight=ft.FontWeight.W_500
                    ),
                    ft.FilledButton(
                        "Вернуться на главный экран",
                        on_click=lambda e: show_main_screen(),
                        icon=Icons.HOME,
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=8),
                        ),
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=30,
            ),
            elevation=5,
        )
    
    #получаем список всех таблиц из БД, исключая UserAuth
    all_tables = ["AppCategories", "ActionTypes", "Devices", "Applications", 
                 "Users", "UserActions", "UserPreferences"]
    
    #текущая выбранная таблица
    current_table = ft.Ref[str]()
    current_table.current = all_tables[0]
    
    #создаем заголовок
    title = ft.Text(
        "Управление данными", 
        size=28, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    #создаем элементы для удаления по ID
    delete_id_field = ft.TextField(
        label="ID записи для удаления",
        width=200,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        prefix_icon=Icons.NUMBERS,
    )
    
    delete_status = ft.Text(
        "",
        size=16,
        color="red",
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_500
    )
    
    #создаем Data Table для отображения содержимого таблицы
    data_table = ft.DataTable(
        columns=[],
        rows=[],
        border=ft.border.all(1, "#BDBDBD"),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, "#E0E0E0"),
        horizontal_lines=ft.border.BorderSide(1, "#E0E0E0"),
        sort_column_index=0,
        heading_row_height=50,
        data_row_min_height=50,
    )
    
    # Оборачиваем таблицу в Column с прокруткой
    data_container = ft.Column(
        [data_table],
        height=400,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )
    
    #функция для обновления записи в таблице
    def update_table_record(record_id, updated_data):
        try:
            #получаем информацию о таблице и первичном ключе
            table_info = db.get_table_info(current_table.current)
            primary_key = table_info['primary_key']
            
            if not primary_key:
                return False, f"Не удалось найти первичный ключ таблицы {current_table.current}"
            
            #подключаемся к БД
            conn, cur = db.connect_db()
            
            try:
                #формируем части запроса
                set_parts = []
                params = []
                
                for column, value in updated_data.items():
                    set_parts.append(f"{column} = ?")
                    params.append(value)
                
                #добавляем условие WHERE
                params.append(record_id)
                
                #формируем запрос
                query = f"UPDATE {current_table.current} SET {', '.join(set_parts)} WHERE {primary_key} = ?"
                
                #выполняем запрос
                cur.execute(query, params)
                conn.commit()
                
                #проверка успешности обновления
                if cur.rowcount > 0:
                    return True, f"Запись с ID {record_id} обновлена успешно"
                else:
                    return False, f"Запись с ID {record_id} не найдена или не изменена"
                    
            except Exception as e:
                conn.rollback()
                return False, f"Ошибка при обновлении: {str(e)}"
            finally:
                conn.close()
                
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    #функция для редактирования записи
    def edit_record_dialog(record_id, record_data, columns):
        #создаем поля ввода для каждого столбца (кроме ID)
        fields = {}
        field_list = []
        
        #получаем информацию о таблице
        table_info = db.get_table_info(current_table.current)
        primary_key = table_info['primary_key']
        
        for i, column in enumerate(columns):
            #для первичного ключа (обычно ID) поле не создаем или делаем его недоступным
            if column == primary_key:
                continue
                
            field = ft.TextField(
                label=column,
                value=str(record_data[i]) if record_data[i] is not None else "",
                border=ft.InputBorder.OUTLINE,
                border_radius=8,
                width=300
            )
            fields[column] = field
            field_list.append(field)
        
        edit_status_text = ft.Text(
            "",
            size=16,
            color="red",
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500
        )
        
        #функция для сохранения изменений
        def save_edited_record(e):
            #собираем данные из полей
            updated_data = {}
            
            for column, field in fields.items():
                if field.value:
                    updated_data[column] = field.value
                else:
                    edit_status_text.value = f"Поле {column} не может быть пустым"
                    edit_status_text.color = "red"
                    page.update()
                    return
            
            #обновляем запись в БД
            try:
                success, message = update_table_record(record_id, updated_data)
                
                if success:
                    page.close(edit_dialog)
                    delete_status.value = message
                    delete_status.color = "green"
                    update_data_table()
                    show_success_snackbar(page, message)
                else:
                    edit_status_text.value = message
                    edit_status_text.color = "red"
                    page.update()
                    show_error_snackbar(page, message)
            except Exception as e:
                error_msg = str(e)
                edit_status_text.value = f"Ошибка:"
                edit_status_text.color = "red"
                page.update()
                show_error_snackbar(page, error_msg)
        
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Редактирование записи с ID {record_id}", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    field_list + [edit_status_text],
                    width=300,
                    height=400,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=10,
            ),
            actions=[
                ft.TextButton(
                    "Отмена", 
                    on_click=lambda e: page.close(edit_dialog)
                ),
                ft.FilledButton(
                    "Сохранить", 
                    on_click=save_edited_record,
                    icon=Icons.SAVE,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(edit_dialog)
    
    #функция для удаления записи
    def delete_table_record(record_id):
        try:
            #получаем информацию о таблице и первичном ключе
            table_info = db.get_table_info(current_table.current)
            primary_key = table_info['primary_key']
            
            if not primary_key:
                delete_status.value = f"Не удалось найти первичный ключ таблицы {current_table.current}"
                delete_status.color = "red"
                page.update()
                show_error_snackbar(page, f"Не удалось найти первичный ключ таблицы {current_table.current}")
                return False
            
            #создаем условие для удаления
            conditions = {primary_key: record_id}
            
            #вызываем функцию удаления из db.py
            deleted_count = db.delete_record(current_table.current, conditions)
            
            if deleted_count and deleted_count > 0:
                delete_status.value = f"Запись с ID {record_id} удалена успешно"
                delete_status.color = "green"
                page.update()
                show_success_snackbar(page, f"Запись с ID {record_id} удалена успешно")
                return True
            else:
                delete_status.value = f"Запись с ID {record_id} не найдена"
                delete_status.color = "red"
                page.update()
                show_error_snackbar(page, f"Запись с ID {record_id} не найдена")
                return False
                
        except Exception as e:
            error_msg = str(e)
            delete_status.value = f"Ошибка при удалении: {error_msg}"
            delete_status.color = "red"
            page.update()
            show_error_snackbar(page, error_msg)
            return False
    
    #функция, вызываемая при нажатии на кнопку удаления по ID
    def delete_by_id_click(e):
        record_id = delete_id_field.value
        
        if not record_id:
            delete_status.value = "Введите ID записи для удаления"
            delete_status.color = "red"
            page.update()
            return
        
        try:
            record_id = int(record_id)
        except ValueError:
            delete_status.value = "ID должен быть числом"
            delete_status.color = "red"
            page.update()
            return
        
        #создаем диалог подтверждения
        def confirm_delete(e):
            #закрываем диалог
            page.close(delete_dialog)
            
            #выполняем удаление
            if delete_table_record(record_id):
                #очищаем поле ID
                delete_id_field.value = ""
                #обновляем таблицу
                update_data_table()
        
        delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Вы уверены, что хотите удалить запись с ID {record_id}?"),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: page.close(delete_dialog)),
                ft.TextButton(
                    "Удалить", 
                    on_click=confirm_delete,
                    style=ButtonStyle(color="red"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(delete_dialog)
    
    #функция для удаления записи через иконку в таблице
    def delete_row_click(e, record_id):
        #создаем диалог подтверждения
        def confirm_delete(e):
            #закрываем диалог
            page.close(delete_dialog)
            
            #выполняем удаление
            if delete_table_record(record_id):
                #обновляем таблицу
                update_data_table()
        
        delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text(f"Вы уверены, что хотите удалить запись с ID {record_id}?"),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: page.close(delete_dialog)),
                ft.TextButton("Удалить", on_click=confirm_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(delete_dialog)
    
    #функция для обработки нажатия кнопки редактирования
    def edit_row_click(e, record_id, row_data, columns):
        edit_record_dialog(record_id, row_data, columns)
    
    #функция для обновления таблицы данных
    def update_data_table():
        if not current_table.current:
            return
            
        #получаем информацию о выбранной таблице
        table_info = db.get_table_info(current_table.current)
        
        #очищаем текущую таблицу
        data_table.columns.clear()
        data_table.rows.clear()
        
        #добавляем заголовки столбцов
        for column in table_info['columns']:
            data_table.columns.append(ft.DataColumn(ft.Text(column)))
        
        #добавляем столбец действий
        data_table.columns.append(ft.DataColumn(ft.Text("Действия")))
        
        #определяем индекс первичного ключа
        primary_key = table_info['primary_key']
        primary_key_index = table_info['columns'].index(primary_key) if primary_key in table_info['columns'] else 0
        
        #добавляем строки данных
        for row in table_info['data']:
            cells = []
            
            #добавляем ячейки с данными
            for value in row:
                #приводим значение к строке и обрабатываем None
                str_value = str(value) if value is not None else ""
                cells.append(ft.DataCell(ft.Text(str_value)))
            
            #получаем ID записи (значение первичного ключа)
            record_id = row[primary_key_index]
            
            #создаем кнопки действий
            edit_button = ft.IconButton(
                icon=Icons.EDIT,
                tooltip="Редактировать запись",
                on_click=lambda e, id=record_id, data=row, cols=table_info['columns']: edit_row_click(e, id, data, cols)
            )
            
            delete_button = ft.IconButton(
                icon=Icons.DELETE,
                tooltip="Удалить запись",
                on_click=lambda e, id=record_id: delete_row_click(e, id)
            )
            
            #добавляем ячейку с кнопками действий
            action_row = ft.Row([edit_button, delete_button], spacing=0)
            cells.append(ft.DataCell(action_row))
            
            #добавляем строку в таблицу
            data_table.rows.append(ft.DataRow(cells=cells))
        
        page.update()
    
    #функция для отображения диалога добавления записи
    def show_add_record_dialog():
        if not current_table.current:
            return
            
        #получаем информацию о столбцах текущей таблицы
        table_info = db.get_table_info(current_table.current)
        columns = table_info['columns']
        
        #создаем поля ввода для каждого столбца (кроме ID)
        fields = {}
        field_list = []
        
        for column in columns:
            #для первичного ключа (обычно ID) поле не создаем
            if column == table_info['primary_key']:
                continue
                
            field = ft.TextField(
                label=column,
                border=ft.InputBorder.OUTLINE,
                border_radius=8,
                width=300
            )
            fields[column] = field
            field_list.append(field)
        
        status_text = ft.Text(
            "",
            size=16,
            color="red",
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.W_500
        )
        
        #функция для сохранения новой записи
        def save_new_record(e):
            #собираем данные из полей
            record_data = {}
            
            for column, field in fields.items():
                #проверяем, что обязательные поля заполнены
                if field.value:
                    record_data[column] = field.value
                else:
                    status_text.value = f"Поле {column} обязательно для заполнения"
                    status_text.color = "red"
                    page.update()
                    return
            
            #добавляем запись в БД
            try:
                db.add_record(current_table.current, record_data)
                page.close(add_dialog)
                update_data_table()
                show_success_snackbar(page, "Запись успешно добавлена")
            except Exception as e:
                error_msg = str(e)
                status_text.value = f"Ошибка:"
                status_text.color = "red"
                page.update()
                show_error_snackbar(page, error_msg)
        
        add_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Добавление записи в таблицу {current_table.current}", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    field_list + [status_text],
                    width=300,
                    height=400,
                    spacing=10,
                    scroll=ft.ScrollMode.AUTO
                ),
                padding=10,
            ),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: page.close(add_dialog)),
                ft.FilledButton(
                    "Сохранить", 
                    on_click=save_new_record,
                    icon=Icons.SAVE,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.open(add_dialog)
    
    #создаем обработчик изменения выбранной таблицы
    def handle_rail_change(e):
        selected_index = e.control.selected_index
        
        #индекс 0 - это кнопка добавления
        if selected_index == 0:
            show_add_record_dialog()
            #возвращаем фокус на последнюю выбранную таблицу
            for i, table in enumerate(all_tables):
                if table == current_table.current:
                    rail.selected_index = i + 1  # +1 из-за кнопки добавления
                    break
            page.update()
            return
        
        #для остальных индексов выбираем соответствующую таблицу
        #индексы сдвинуты на 1 из-за кнопки добавления
        table_index = selected_index - 1
        if table_index < len(all_tables):
            current_table.current = all_tables[table_index]
            title.value = f"Таблица: {current_table.current}"
            #очищаем поле ID и статус при смене таблицы
            delete_id_field.value = ""
            delete_status.value = ""
            update_data_table()
            page.update()
    
    #создаем навигационную панель
    rail_destinations = [
        ft.NavigationRailDestination(
            icon=Icons.ADD_CIRCLE_OUTLINE,
            selected_icon=Icons.ADD_CIRCLE,
            label="Добавить"
        )
    ]
    
    #добавляем кнопки для каждой таблицы
    for table in all_tables:
        rail_destinations.append(
            ft.NavigationRailDestination(
                icon=Icons.TABLE_CHART_OUTLINED,
                selected_icon=Icons.TABLE_CHART,
                label=table
            )
        )
    
    rail = ft.Container(
        content=ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=120,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=rail_destinations,
            on_change=handle_rail_change,
            bgcolor="fafafaf",
        ),
        height=800,  # Фиксированная высота
    )
    
    #кнопка для возврата на главный экран
    back_button = ft.FilledTonalButton(
        "Вернуться на главный экран",
        on_click=lambda e: show_main_screen(),
        icon=Icons.HOME,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
    )
    
    #кнопка удаления по ID
    delete_button = ft.FilledButton(
        "Удалить по ID",
        on_click=delete_by_id_click,
        icon=Icons.DELETE,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
            color="#F44336",
        ),
    )
    
    #создаем форму для удаления по ID
    delete_form = ft.Row(
        [
            delete_id_field,
            delete_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )
    
    #показываем первую таблицу при инициализации
    current_table.current = all_tables[0]
    title.value = f"Таблица: {current_table.current}"
    update_data_table()
    
    #создаем основной контент панели оператора
    content = ft.Container(
        content=ft.Column(
            [
                title,
                ft.Divider(height=10, color="transparent"),
                data_container,
                ft.Divider(height=20, color="transparent"),
                delete_form,
                delete_status,
                ft.Divider(height=20, color="transparent"),
                back_button
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
            expand=True,
        ),
        padding=20,
        expand=True,
    )
    
    #собираем весь интерфейс
    return ft.Card(
        content=ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1, thickness=1, color="#E0E0E0"),
                content
            ],
            expand=True
        ),
        elevation=5,
        surface_tint_color="#E0E0E0",
        margin=20,
    )

def admin_tables_view(page):
    #проверка прав доступа
    def check_permission():
        return session.is_authenticated and session.role == "админ"
        
    def show_main_screen():
        page.controls.clear()
        page.add(hello_user_page(page))
        page.update()
    
    if not check_permission():
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "У вас нет прав для доступа к этой панели", 
                        size=20, 
                        color="red",
                        weight=ft.FontWeight.W_500
                    ),
                    ft.FilledButton(
                        "Вернуться на главный экран",
                        on_click=lambda e: show_main_screen(),
                        icon=Icons.HOME,
                        style=ButtonStyle(
                            shape=RoundedRectangleBorder(radius=8),
                        ),
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                padding=30,
            ),
            elevation=5,
        )
    
    #получаем список всех таблиц из БД, исключая UserAuth
    all_tables = ["AppCategories", "ActionTypes", "Devices", "Applications", 
                 "Users", "UserActions", "UserPreferences"]
    
    #текущая выбранная таблица
    current_table = ft.Ref[str]()
    current_table.current = all_tables[0]
    
    #создаем заголовок
    title = ft.Text(
        "Просмотр таблиц (режим администратора)", 
        size=28, 
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    #создаем Data Table для отображения содержимого таблицы
    data_table = ft.DataTable(
        columns=[],
        rows=[],
        border=ft.border.all(1, "#BDBDBD"),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, "#E0E0E0"),
        horizontal_lines=ft.border.BorderSide(1, "#E0E0E0"),
        sort_column_index=0,
        heading_row_height=50,
        data_row_min_height=50,
    )
    
    # Оборачиваем таблицу в Column с прокруткой вместо Container
    data_container = ft.Column(
        [data_table],
        height=400,
        expand=True,
        scroll=ft.ScrollMode.AUTO
    )
    
    #функция для обновления таблицы данных
    def update_data_table():
        if not current_table.current:
            return
            
        #получаем информацию о выбранной таблице
        table_info = db.get_table_info(current_table.current)
        
        #очищаем текущую таблицу
        data_table.columns.clear()
        data_table.rows.clear()
        
        #добавляем заголовки столбцов
        for column in table_info['columns']:
            data_table.columns.append(ft.DataColumn(
                ft.Text(column, weight=ft.FontWeight.BOLD)
            ))
        
        #добавляем строки данных
        for row in table_info['data']:
            cells = []
            for value in row:
                #приводим значение к строке и обрабатываем None
                str_value = str(value) if value is not None else ""
                cells.append(ft.DataCell(ft.Text(str_value)))
            
            data_table.rows.append(ft.DataRow(cells=cells))
        
        page.update()
    
    #создаем обработчик изменения выбранной таблицы
    def handle_rail_change(e):
        selected_index = e.control.selected_index
        
        #обновляем текущую таблицу
        if selected_index < len(all_tables):
            current_table.current = all_tables[selected_index]
            title.value = f"Таблица: {current_table.current} (режим просмотра)"
            update_data_table()
            page.update()
    
    #создаем навигационную панель
    rail_destinations = []
    
    #добавляем кнопки для каждой таблицы
    for table in all_tables:
        rail_destinations.append(
            ft.NavigationRailDestination(
                icon=Icons.TABLE_CHART_OUTLINED,
                selected_icon=Icons.TABLE_CHART,
                label=table
            )
        )
    
    rail = ft.Container(
        content=ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=120,
            min_extended_width=200,
            group_alignment=-0.9,
            destinations=rail_destinations,
            on_change=handle_rail_change,
            bgcolor="fafafaf",
        ),
        height=800,  # Фиксированная высота
    )
    
    #кнопка для возврата на главный экран
    back_button = ft.FilledTonalButton(
        "Вернуться на главный экран",
        on_click=lambda e: show_main_screen(),
        icon=Icons.HOME,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
        ),
    )
    
    #показываем первую таблицу при инициализации
    current_table.current = all_tables[0]
    title.value = f"Таблица: {current_table.current} (режим просмотра)"
    update_data_table()
    
    #создаем основной контент панели администратора
    content = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    title,
                    ft.Divider(height=10, color="transparent"),
                    data_container,
                    ft.Divider(height=20, color="transparent"),
                    back_button
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=10,
                expand=True,
            ),
            padding=20,
            expand=True,
        ),
        elevation=5,
        surface_tint_color="#E0E0E0",
        margin=20,
    )
    
    #собираем весь интерфейс
    return ft.Card(
        content=ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1, thickness=1, color="#E0E0E0"),
                content
            ],
            expand=True
        ),
        elevation=5,
        surface_tint_color="#E0E0E0",
        margin=20,
    )


ft.app(target=login_page)