import flet as ft
from partials.sidebar import Sidebar
from partials.content import MainContent


def AdminPage(page: ft.Page):
    page.title = "Painel Alison dev"

    sidebar = Sidebar()
    content = MainContent()

    return ft.ResponsiveRow(
        controls=[
            ft.Column(col={"sm": 0, "xl": 4}, controls=[sidebar], expand=False),
            ft.Column(col={"sm": 12, "xl": 8}, controls=[content], expand=True),
        ],
        spacing=20,
        expand=True
    )
