import flet as ft
from services import Fetch  # Supondo que você tenha uma função para buscar os dados

def AdminPage(page: ft.Page):
    page.title = "Administração"

    # Função para tratar o logout
    def handle_logout(e):
        page.go("/login")
    # Layout do dashboard
    return ft.Column(
        controls=[
            ft.Text(value="Administração", size=30, weight=ft.FontWeight.W_900),
            ft.ElevatedButton(
                text="Logout",
                on_click=handle_logout
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )
