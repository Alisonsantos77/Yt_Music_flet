import flet as ft
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.admin_page import AdminPage
from pages.adminregister_page import AdminRegisterPage
from loguru import logger


def setup_routes(page: ft.Page):
    logger.info("Configurando rotas")
    page.theme = ft.Theme(
        page_transitions={'windows': ft.PageTransitionTheme.ZOOM},
    )

    def route_change(route):
        logger.info(f"Rota alterada: {route}")
        page.views.clear()
        page.views.append(
            ft.View(
                route="/login",
                controls=[LoginPage(page)],
            )
        )
        logger.info("Página de Login carregada")

        if page.route == "/adminregister":
            page.views.append(
                ft.View(
                    "/adminregister",
                    [
                        AdminRegisterPage(page)
                    ],
                )
            )
            logger.info("Página de Registro de Admin carregada")

        if page.route == "/register":
            page.views.append(
                ft.View(
                    "/register",
                    [
                        RegisterPage(page)
                    ],
                )
            )
            logger.info("Página de Registro carregada")

        if page.route == "/admin":
            page.views.append(
                ft.View(
                    "/admin",
                    [
                        AdminPage(page)
                    ],
                )
            )
            logger.info("Página de Admin carregada")

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
            logger.info("Página Home carregada")

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        logger.info(f"Retornando para a rota anterior: {top_view.route}")
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
