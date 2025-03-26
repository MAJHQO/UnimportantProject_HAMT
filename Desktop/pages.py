import flet as ft


def start_page(page:ft.Page):

    page.window.width=800
    page.window.height=700

    page.title="НАМТ.Администраторы"
    page.horizontal_alignment=ft.MainAxisAlignment.CENTER
    page.vertical_alignment=ft.CrossAxisAlignment.CENTER
    page.theme_mode=ft.ThemeMode.LIGHT
    page.window.resizable=False

    page.update()

def startAdmin_page(page:ft.Page):

    page.clean()
    page.update()

    page.window.width=800
    page.window.height=700

    page.title="НАМТ.Администраторы"
    page.theme_mode=ft.ThemeMode.LIGHT
    page.window.resizable=False

    loginField=ft.TextField(label="Логин",hint_text="Логин", width=180)
    passwordField=ft.TextField(label="Пароль",hint_text="Пароль", width=180, password=True)
    regirtrAdminButton=ft.ElevatedButton("Зарегистрироваться", width=165)

    page.add(ft.Column([loginField,passwordField,regirtrAdminButton], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=800,height=700))
    page.update()