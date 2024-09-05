import flet as ft
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.admin_page import AdminPage


def setup_routes(page: ft.Page):
    # Configuração do tema da página
    page.theme = ft.Theme(
        page_transitions={'windows': ft.PageTransitionTheme.ZOOM},
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                route="/login",
                controls=[
                    LoginPage(page)
                ],
            )
        )
        if page.route == "/register":
            page.views.append(
                ft.View(
                    "/register",
                    [
                        RegisterPage(page)
                    ],
                )
            )
        if page.route == "/admin":
            page.views.append(
                ft.View(
                    "/admin",
                    [
                        AdminPage(page)
                    ],
                )
            )
        if page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    [
                        ft.AppBar(title=ft.Text("Home aqui"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Voltar login", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
