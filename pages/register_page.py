import flet as ft
from utils.validations import validate_register
from services import Commit

def RegisterPage(page: ft.Page):
    page.bgcolor = ft.colors.GREEN_50

    # Campos de entrada de dados
    input_username = ft.TextField(hint_text='Nome de usuário')
    input_email = ft.TextField(hint_text='Insira seu email')
    input_senha = ft.TextField(hint_text='Insira sua senha', password=True, can_reveal_password=True)
    input_confirm_senha = ft.TextField(hint_text='Confirme sua senha', password=True, can_reveal_password=True)

    def handle_register(e):
        username = input_username.value
        email = input_email.value
        password = input_senha.value
        confirm_password = input_confirm_senha.value

        # Validando os campos de registro
        is_valid, error_message = validate_register(username, email, password, confirm_password)
        print(f"Validando registro: is_valid={is_valid}, error_message={error_message}")
        if not is_valid:
            page.snack_bar = ft.SnackBar(content=ft.Text(error_message))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Commit da solicitação de registro na tabela `registration_requests`
            Commit.commit_registration_request(
                data={
                    'username': username,
                    'email': email,
                    'password': password,
                }
            )

            page.snack_bar = ft.SnackBar(content=ft.Text("Solicitação de registro enviada com sucesso! Aguarde aprovação."))
            page.snack_bar.open = True
            page.update()

            # Navegar para a página de login após envio da solicitação
            page.go('/login')

        except Exception as error:
            # Tratar qualquer erro que possa ocorrer
            print(f"Erro ao enviar solicitação de registro: {error}")
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao registrar: {str(error)}"))
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
                controls=[
                    ft.Text(
                        value='Bem-vindo ao Alison Dev',
                        size=32,
                        color=ft.colors.WHITE,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        value='Crie sua conta para começar a explorar nossos serviços.',
                        size=16,
                        color=ft.colors.WHITE70,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    input_username,
                    input_email,
                    input_senha,
                    input_confirm_senha,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton(
                                "REGISTRAR",
                                icon=ft.icons.DOOR_FRONT_DOOR,
                                on_click=handle_register  # Adiciona o evento de clique
                            ),
                        ],
                    ),
                    ft.TextButton(
                        text="Já possui uma conta? Faça login.",
                        style=ft.ButtonStyle(
                            color=ft.colors.CYAN_200,
                        ),
                        on_click=lambda _: page.go('/login'),
                    )
                ]
            )
        )
    )
