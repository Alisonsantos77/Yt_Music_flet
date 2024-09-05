import flet as ft
from utils.validations import validate_login
from services import Fetch, Commit
from flet.security import decrypt
from config import SECRET_KEY
from loguru import logger


def LoginPage(page: ft.Page):
    new_avatar = ft.Ref[ft.CircleAvatar]()

    def generator_avatar(e):
        if not input_username.value:
            new_avatar.current.foreground_image_src = "https://robohash.org/userdefault.png"
            new_avatar.current.content = ft.Text("", size=30, weight=ft.FontWeight.BOLD)
        else:
            new_avatar.current.foreground_image_src = f"https://robohash.org/{input_username.value}.png"
            new_avatar.current.content = ft.Text(input_username.value[0].upper(), size=30, weight=ft.FontWeight.BOLD)
        new_avatar.current.update()

    # Inicializa o avatar com um CircleAvatar vazio
    avatar = ft.Container(
        content=ft.Row(
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://robohash.org/userdefault.png",
                    content=ft.Text("FF"),
                    width=100,
                    height=100,
                    ref=new_avatar
                )
            ]
        ),
        col={"sm": 5, "md": 4, "xl": 12},
    )

    def register_redirect(e):
        page.go('/register')

    # Campos de entrada de dados
    input_username = ft.TextField(
        hint_text='Insira seu nome de usuário',
        col={"sm": 8, "md": 12, "xl": 12},
        on_change=generator_avatar,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
    )

    input_senha = ft.TextField(
        hint_text='Insira sua senha',
        password=True,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        can_reveal_password=True,
        col={"sm": 8, "md": 12, "xl": 12},
    )

    password_reset_btn = ft.TextButton(
        text='Esqueceu sua senha?',
        icon_color=ft.colors.BLACK12,
        col={"sm": 8, "md": 12, "xl": 12},
        on_click=lambda _: print('Resetar senha')
    )
    new_account_btn = ft.TextButton(
        text='Criar nova conta',
        col={"sm": 8, "md": 12, "xl": 12},
        style=ft.ButtonStyle(
            color=ft.colors.BLACK,
            elevation=2,
            overlay_color=ft.colors.TRANSPARENT
        ),
        on_click=register_redirect
    )

    # Função para tratar o evento de login

    def handle_login(e):
        username = input_username.value
        password = input_senha.value

        # Validação dos campos de login
        is_valid, error_message = validate_login(username, password)
        if not is_valid:
            logger.warning(f"Falha na validação do login para {username}: {error_message}")
            # Exibindo a mensagem retornada pelo validate_login
            page.snack_bar = ft.SnackBar(content=ft.Text(error_message))
            page.snack_bar.open = True
            page.update()
            return

        try:
            # Verificar se o admin existe
            admin = Fetch.fetch_admin_by_username(username)

            if admin is not None:
                decrypted_admin_password = decrypt(admin['password'], SECRET_KEY)

                if decrypted_admin_password == password:
                    # Armazenar o ID do admin na sessão
                    page.session.set("admin_id", admin['id'])
                    page.session.set("admin_username", admin['username'])

                    logger.info(f"Login bem-sucedido para o administrador: {username}, ID: {admin['id']}")

                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f'Bem-vindo de volta, {username}!', size=20, color=ft.colors.BLUE,
                                        weight=ft.FontWeight.W_600)
                    )
                    page.snack_bar.open = True
                    page.update()
                    page.go('/admin')
                else:
                    logger.warning(f"Senha incorreta para o administrador: {username}")
                    page.snack_bar = ft.SnackBar(content=ft.Text("Senha incorreta. Tente novamente."))
                    page.snack_bar.open = True
                    page.update()
            else:
                logger.warning(f"Usuário {username} não encontrado")
                page.snack_bar = ft.SnackBar(content=ft.Text("Usuário não encontrado. Verifique o nome de usuário."))
                page.snack_bar.open = True
                page.update()

        except Exception as ex:
            logger.error(f"Erro ao efetuar login para o usuário {username}: {ex}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value=f"Erro ao efetuar login: {ex}",
                    size=20,
                    color=ft.colors.RED,
                    weight=ft.FontWeight.W_600
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
                                        value="Bem-vindo de volta!",
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
                            input_senha,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.END,
                                controls=[
                                    password_reset_btn
                                ]
                            ),
                            ft.ElevatedButton(
                                text="Acessar conta",
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
                                on_click=handle_login
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    new_account_btn
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
