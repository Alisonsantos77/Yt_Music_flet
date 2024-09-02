import flet as ft
from utils.validations import validate_login
from services import Fetch, Commit


def LoginPage(page: ft.Page):
    page.bgcolor = ft.colors.GREEN_50

    # Campos de entrada de dados
    input_username = ft.TextField(hint_text='Insira seu nome de usuário')
    input_email = ft.TextField(hint_text='Insira seu email')
    input_senha = ft.TextField(hint_text='Insira sua senha', password=True, can_reveal_password=True)

    # Função para tratar o evento de login
    def handle_login(e):
        username = input_username.value
        email = input_email.value
        password = input_senha.value

        # Validando os campos de login
        is_valid, error_message = validate_login(username, email, password)
        print(f"Validando login: is_valid={is_valid}, error_message={error_message}")
        if not is_valid:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value=error_message, size=20,
                    color=ft.colors.RED,
                    weight=ft.FontWeight.W_600,
                    italic=True)
            )
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Verificar se o usuário existe e a senha corresponde
            user = Fetch.fetch_user_by_username(username)

            # Verificar se o admin existe e a senha corresponde
            admin = Fetch.fetch_admin_by_username(username)

            if admin is not None and admin['password'] == password and admin['email'] == email:
                # Caso o usuário seja administrador
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        value=f'{username} entrou como administrador',
                        size=20,
                        color=ft.colors.BLUE,
                        weight=ft.FontWeight.W_600,
                        italic=True
                    )
                )
                page.snack_bar.open = True
                page.update()
                page.go('/admin')
            elif user is not None and user['password'] == password and user['email'] == email:
                Commit.update_last_login(user['id'])

                page.snack_bar = ft.SnackBar(
                    content=ft.Text(
                        value='Login realizado com sucesso',
                        size=20,
                        color=ft.colors.BLUE,
                        weight=ft.FontWeight.W_600,
                        italic=True
                    )
                )
                page.snack_bar.open = True
                page.update()
                page.go('/home')
            else:
                print("Nome de usuário ou senha incorretos")
                raise Exception("Nome de usuário ou senha incorretos")

        except ValueError as ve:
            print(f"Erro de valor: {ve}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value=str(ve),
                    size=20,
                    color=ft.colors.RED,
                    weight=ft.FontWeight.W_600,
                    italic=True
                )
            )
            page.snack_bar.open = True
            page.update()

        except Exception as ex:
            print(f"Erro ao efetuar login: {ex}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value=f"Erro ao efetuar login: {ex}",
                    size=20,
                    color=ft.colors.RED,
                    weight=ft.FontWeight.W_600,
                    italic=True
                )
            )
            page.snack_bar.open = True
            page.update()

    # Layout da página
    return ft.Container(
        image_src='https://images3.alphacoders.com/133/1332803.png',
        image_fit=ft.ImageFit.COVER,
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            padding=ft.padding.symmetric(vertical=50, horizontal=80),
            border_radius=ft.border_radius.all(10),
            blur=ft.Blur(sigma_x=8, sigma_y=8),
            height=600,
            aspect_ratio=9 / 16,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            border=ft.Border(
                top=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                right=ft.BorderSide(width=2, color=ft.colors.WHITE30),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value='Bem-vindo de volta!',
                        size=32,
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        value='Entre com suas credenciais para acessar sua conta.',
                        size=16,
                        color=ft.colors.WHITE70,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    input_username,
                    input_email,
                    input_senha,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                "ENTRAR",
                                icon=ft.icons.DOOR_FRONT_DOOR,
                                on_click=handle_login  # Adiciona o evento de clique
                            ),
                        ],
                    ),
                    ft.TextButton(
                        text="Não possui uma conta? Registre-se.",
                        style=ft.ButtonStyle(
                            color=ft.colors.CYAN_200,
                        ),
                        on_click=lambda _: page.go('/register'),
                    )
                ],
                spacing=20
            )
        )
    )
