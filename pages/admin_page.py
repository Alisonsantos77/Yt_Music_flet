import flet as ft
from partials.content import MainContent
from partials.sidebar import Sidebar

def AdminPage(page: ft.Page):
    page.title = "Administração"

    sidebar = Sidebar(col={'xs': 0, 'md': 5, 'lg': 4, 'xxl': 3})
    main = MainContent(col={'xs': 12, 'md': 7, 'lg': 8, 'xxl': 9})

    # Layout do dashboard
    return ft.Column(
        controls=[
            sidebar,
            main,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
