import flet as ft

class HomePage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.create_layout()

    def create_layout(self):
        layout = ft.Column(
            controls=[
                ft.Text(value="Bem-vindo à Página Principal!", size=30, weight=ft.FontWeight.W_900),
                ft.ElevatedButton(
                    text="Logout",
                    on_click=self.handle_logout
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.add(layout)

    def handle_logout(self, e):
        self.page.go("/")
