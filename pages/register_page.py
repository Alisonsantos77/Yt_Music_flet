import flet as ft
from utils.validations import validate_register
from services import Commit, Fetch
from flet.security import encrypt
from config import SECRET_KEY
from loguru import logger


def RegisterPage(page: ft.Page):
    new_avatar = ft.Ref[ft.CircleAvatar]()

    def generator_avatar(e):
        if not input_username.value:
            new_avatar.current.foreground_image_src = "https://robohash.org/userdefault.png"
            new_avatar.current.content = ft.Text("A", size=30, weight=ft.FontWeight.BOLD)
        else:
            new_avatar.current.foreground_image_src = f"https://robohash.org/{input_username.value}.png"
            new_avatar.current.content = ft.Text(input_username.value[0].upper(), size=30, weight=ft.FontWeight.BOLD)
        new_avatar.current.update()

    avatar = ft.Container(
        content=ft.Row(
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://robohash.org/userdefault.png",
                    content=ft.Text("A", size=30, weight=ft.FontWeight.BOLD),
                    width=100,
                    height=100,
                    ref=new_avatar
                )
            ]
        ),
        col={"sm": 5, "md": 4, "xl": 12},
    )

    def login_redirect(e):
        page.go('/login')

    input_username = ft.TextField(
        hint_text='Insira seu nome de usuário',
        col={"sm": 8, "md": 12, "xl": 12},
        on_change=generator_avatar,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
    )
    input_email = ft.TextField(
        hint_text='Insira seu email',
        col={"sm": 8, "md": 12, "xl": 12},
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
    )

    input_senha = ft.TextField(
        hint_text='Crie uma senha',
        password=True,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        can_reveal_password=True,
        col={"sm": 8, "md": 12, "xl": 12},
    )
    input_senha_confirm = ft.TextField(
        hint_text='Confirme sua senha',
        password=True,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        can_reveal_password=True,
        col={"sm": 8, "md": 12, "xl": 12},
    )

    have_account = ft.TextButton(
        text='Já possui uma conta?',
        col={"sm": 8, "md": 12, "xl": 12},
        style=ft.ButtonStyle(
            color=ft.colors.BLUE_700,
            elevation=2,
            overlay_color=ft.colors.TRANSPARENT
        ),
        on_click=login_redirect
    )

    def handle_register(e):
        username = input_username.value
        email = input_email.value
        password = input_senha.value
        confirm_password = input_senha_confirm.value

        # Logando início do processo de registro
        logger.info(f"Tentativa de registro para o usuário: {username}")

        # Validação dos campos
        is_valid, error_message = validate_register(username, email, password, confirm_password)
        if not is_valid:
            logger.warning(f"Falha na validação do registro para {username}: {error_message}")
            page.snack_bar = ft.SnackBar(content=ft.Text(error_message))  # Usa a mensagem humanizada
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Criptografando a senha
            encrypted_password = encrypt(password, SECRET_KEY)
            logger.info(f"Senha criptografada para {username}")

            # Inserindo o usuário na tabela `registration_requests` com status 'pending'
            Commit.commit_registration_request(
                data={
                    'username': username,
                    'email': email,
                    'password': encrypted_password,
                    'status': 'pending',  # Define o status como 'pending'
                    'reviewed_by_admin_id': None  # Nenhum admin revisou ainda
                }
            )

            logger.info(f"Usuário {username} registrado na tabela de requests com status 'pending'.")

            # Notificando o sucesso
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Cadastro enviado para revisão. Aguarde a aprovação de um administrador!"))
            page.snack_bar.open = True
            page.update()

            # Redirecionar para a página de login
            page.go('/login')

        except Exception as error:
            logger.error(f"Erro ao registrar a solicitação de {username}: {error}")
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Desculpe, ocorreu um erro durante o cadastro: {str(error)}"))
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        image_src='https://images3.alphacoders.com/133/1332803.png',
        image_fit=ft.ImageFit.COVER,
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            padding=ft.padding.symmetric(vertical=50, horizontal=80),
            border_radius=ft.border_radius.all(10),
            blur=ft.Blur(sigma_x=8, sigma_y=8),
            aspect_ratio=9 / 16,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            border=ft.Border(
                top=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                right=ft.BorderSide(width=2, color=ft.colors.WHITE30),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                controls=[
                    ft.ResponsiveRow(
                        col={"sm": 10, "md": 4, "xl": 12},
                        controls=[
                            ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            avatar
                                        ]
                                    ),
                                    ft.Text(
                                        value="Crie sua conta",
                                        size=20,
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.BOLD,
                                        col={"sm": 5, "md": 4, "xl": 12},
                                    ),
                                ]
                            ),
                        ],
                    ),
                    ft.ResponsiveRow(
                        col={"sm": 10, "md": 12, "xl": 12},
                        controls=[
                            input_username,
                            input_email,
                            input_senha,
                            input_senha_confirm,
                            ft.ElevatedButton(
                                text="Cadastrar",
                                style=ft.ButtonStyle(
                                    padding=ft.padding.all(10),
                                    bgcolor={
                                        ft.MaterialState.HOVERED: ft.colors.PRIMARY,
                                    },
                                    color={
                                        ft.MaterialState.DEFAULT: ft.colors.WHITE,
                                        ft.MaterialState.HOVERED: ft.colors.BLACK,

                                    }
                                ),
                                on_click=handle_register
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    have_account
                                ]
                            ),
                        ],
                        run_spacing={"xs": 10},
                    ),
                ],
                spacing=20
            )
        )
    )
