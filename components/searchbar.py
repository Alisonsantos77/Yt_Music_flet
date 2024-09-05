import flet as ft
from services import Fetch  # Importa Fetch para usar no filtro


class SearchBarItem(ft.UserControl):
    def __init__(self, on_search_results, placeholder: str = "Digite sua pesquisa...", **kwargs):
        super().__init__(**kwargs)
        self.on_search_results = on_search_results  # Função para atualizar a tabela no MainContent
        self.placeholder = placeholder

    def search_user(self, query):
        # Filtra os usuários com base no username ou email
        filtered_users = [user for user in Fetch.users if query.lower() in user['username'].lower() or query.lower() in user['email'].lower()]
        return filtered_users

    def handle_change(self, e):
        query = e.data.strip()
        if query:
            search_results = self.search_user(query)
            self.on_search_results(search_results)  # Atualiza a tabela com os resultados
        else:
            self.on_search_results(None)  # Se a query estiver vazia, exibe todos os usuários

    def build(self):
        return ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=50, horizontal=80),
                border_radius=ft.border_radius.all(10),
                blur=ft.Blur(sigma_x=8, sigma_y=8),
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                border=ft.Border(
                    top=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                    right=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                ),
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.SearchBar(
                                    bar_hint_text=self.placeholder,
                                    width=300,
                                    view_elevation=4,
                                    view_bgcolor=ft.colors.BACKGROUND,
                                    on_change=self.handle_change,  # Usamos a função handle_change
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SEARCH_ROUNDED,
                                )
                            ]
                        ),
                    ]
                )
            )
        )
