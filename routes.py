import flet as ft
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.admin_page import AdminPage
from pages.adminregister_page import AdminRegisterPage
from pages.welcome_page import WelcomePage
from pages.adminlogin_page import AdminLoginPage
from pages.encrypt_test import TestEncryptPage
from loguru import logger


def setup_routes(page: ft.Page):
    logger.info("Configurando rotas")
    page.theme = ft.Theme(
        page_transitions={'windows': ft.PageTransitionTheme.FADE_UPWARDS},
    )

    def route_change(route):
        logger.info(f"Rota alterada: {route}")
        page.views.clear()

        # Página de boas-vindas (sem botão de voltar)
        page.views.append(
            ft.View(
                route="/",
                controls=[WelcomePage(page)],
            )
        )
        logger.info("Página de Boas-vindas carregada")

        # Página de login de usuário
        if page.route == "/login":
            page.views.append(
                ft.View(
                    route="/login",
                    appbar=ft.AppBar(),

                    controls=[
                        LoginPage(page)
                    ],
                )
            )
            logger.info("Página de Login do Usuário carregada")

        # Página de login de admin
        elif page.route == "/adminlogin":
            page.views.append(
                ft.View(
                    route="/adminlogin",
                    appbar=ft.AppBar(),
                    controls=[

                        AdminLoginPage(page)],
                )
            )
            logger.info("Página de Login do Admin carregada")

        # Página de registro de admin
        elif page.route == "/adminregister":
            page.views.append(
                ft.View(
                    route="/adminregister",
                    appbar=ft.AppBar(),

                    controls=[
                        AdminRegisterPage(page)],
                )
            )
            logger.info("Página de Registro de Admin carregada")

        # Página de registro de usuário
        elif page.route == "/register":
            page.views.append(
                ft.View(
                    route="/register",
                    appbar=ft.AppBar(),

                    controls=[
                        RegisterPage(page)],
                )
            )
            logger.info("Página de Registro carregada")

        # Página de Admin
        elif page.route == "/admin":
            page.views.append(
                ft.View(
                    route="/admin",
                    appbar=ft.AppBar(),

                    controls=[
                        AdminPage(page)],
                )
            )
            logger.info("Página de Admin carregada")

        # Página Home
        elif page.route == "/home":
            page.views.append(
                ft.View(
                    route="/home",
                    appbar=ft.AppBar(),

                    controls=[
                        ft.Text("Bem-vindo à página Home!"),
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
