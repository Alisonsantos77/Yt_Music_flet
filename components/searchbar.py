import flet as ft


def handle_change(e):
    print(f"handle_change e.data: {e.data}")


def handle_submit(e):
    print(f"handle_submit e.data: {e.data}")


class SearchBarItem(ft.UserControl):
    def __init__(self, placeholder: str = "Digite sua pesquisa...", button_text: str = "Pesquisar", **kwargs):
        super().__init__(**kwargs)
        self.placeholder = placeholder
        self.button_text = button_text

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
                                    on_change=handle_change,
                                    on_submit=handle_submit,
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

    def on_search_click(self, e):
        # Aqui você pode adicionar a lógica para realizar a pesquisa quando o botão é clicado
        print("Botão de pesquisa clicado!")
