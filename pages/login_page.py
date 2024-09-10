import flet as ft
from utils.validations import validate_login
from services import Fetch, Commit
from flet.security import decrypt
from config import SECRET_KEY
from loguru import logger
from datetime import datetime, timezone


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
        col={"sm": 8, "md": 12, "xl": 5},
        on_change=generator_avatar,
        border=ft.InputBorder.UNDERLINE,
    )

    input_senha = ft.TextField(
        hint_text='Insira sua senha',
        password=True,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        can_reveal_password=True,
        col={"sm": 8, "md": 12, "xl": 5},
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
            color={
                ft.ControlState.DEFAULT: ft.colors.WHITE,
                ft.ControlState.HOVERED: ft.colors.BLACK,
            },
            elevation=2,
            overlay_color=ft.colors.TRANSPARENT
        ),
        on_click=register_redirect
    )

    def handle_login(e):
        username = input_username.value
        password = input_senha.value

        is_valid, error_message = validate_login(username, password)
        if not is_valid:
            logger.warning(f"Falha na validação do login para {username}: {error_message}")
            page.snack_bar = ft.SnackBar(content=ft.Text(error_message, size=20,
                                                         color=ft.colors.RED,
                                                         weight=ft.FontWeight.W_600,
                                                         italic=True))
            page.snack_bar.open = True
            page.update()
            return

        try:
            user = Fetch.fetch_user_by_username(username)

            if user is not None:
                try:
                    encrypted_password = user['password']
                    stored_password = decrypt(encrypted_password, SECRET_KEY)
                except Exception as ex:
                    logger.error(f"Erro ao descriptografar a senha para o usuário {username}: {ex}")
                    page.snack_bar = ft.SnackBar(content=ft.Text("Erro na autenticação. Tente novamente.", size=20,
                                                                 color=ft.colors.RED,
                                                                 weight=ft.FontWeight.W_600,
                                                                 italic=True))
                    page.snack_bar.open = True
                    page.update()
                    return

                # Compara a senha inserida pelo usuário com a senha armazenada
                if stored_password == password:
                    page.session.set("user_id", user['id'])
                    page.session.set("user_username", user['username'])
                    logger.info(f"Login bem-sucedido para o usuário: {username}")

                    # Atualiza o campo last_login no banco de dados
                    last_login_time = datetime.now(timezone.utc).isoformat()
                    Commit.update_last_login(user['id'], last_login_time)
                    logger.info(f"last_login atualizado para o usuário {username}")

                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f'Bem-vindo de volta, {username}!', size=20, color=ft.colors.BLUE,
                                        weight=ft.FontWeight.W_600)
                    )
                    page.snack_bar.open = True
                    page.update()

                    page.go('/home')
                else:
                    logger.warning(f"Tentativa de login falhou para {username}: senha incorreta")
                    page.snack_bar = ft.SnackBar(content=ft.Text("Usuário ou senha incorretos. Tente novamente."))
                    page.snack_bar.open = True
                    page.update()
            else:
                logger.warning(f"Usuário {username} não encontrado")
                page.snack_bar = ft.SnackBar(content=ft.Text("Usuário ou senha incorretos. Tente novamente."))
                page.snack_bar.open = True
                page.update()

        except Exception as ex:
            logger.error(f"Erro ao processar o login para {username}: {ex}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value=f"Erro ao efetuar login. Tente novamente.",
                    size=20,
                    color=ft.colors.RED,
                    weight=ft.FontWeight.W_600
                )
            )
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            border_radius=ft.border_radius.all(10),
            blur=ft.Blur(sigma_x=8, sigma_y=8),
            margin=20,
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
                                        overflow=ft.TextOverflow.ELLIPSIS,
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
                        alignment=ft.MainAxisAlignment.CENTER,
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
                                        ft.ControlState.HOVERED: ft.colors.WHITE,
                                    },
                                    color={
                                        ft.ControlState.DEFAULT: ft.colors.WHITE,
                                        ft.ControlState.HOVERED: ft.colors.BLACK,
                                    },
                                    elevation={"pressed": 0, "": 1},
                                    animation_duration=500,
                                    shape=ft.RoundedRectangleBorder(radius=6),
                                ),
                                on_click=handle_login,
                                col={"sm": 8, "md": 10, "xl": 6},
                            ),
                            ft.ResponsiveRow(
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
