import flet as ft
from utils.validations import validate_login
from services import Fetch
from flet.security import decrypt
from config import SECRET_KEY
from loguru import logger


def AdminLoginPage(page: ft.Page):
    new_avatar = ft.Ref[ft.CircleAvatar]()

    # Função para gerar o avatar dinamicamente
    def generator_avatar(e):
        if not input_username.value:
            new_avatar.current.foreground_image_src = "https://robohash.org/admindefault.png"
            new_avatar.current.content = ft.Text("", size=30, weight=ft.FontWeight.BOLD)
        else:
            new_avatar.current.foreground_image_src = f"https://robohash.org/{input_username.value}.png"
            new_avatar.current.content = ft.Text(input_username.value[0].upper(), size=30, weight=ft.FontWeight.BOLD)
        new_avatar.current.update()

    # Avatar padrão
    avatar = ft.Container(
        content=ft.Row(
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://robohash.org/admindefault.png",
                    content=ft.Text("A"),
                    width=100,
                    height=100,
                    ref=new_avatar
                )
            ]
        ),
        col={"sm": 5, "md": 4, "xl": 12},
    )

    # Campos de entrada para login
    input_username = ft.TextField(
        hint_text='Digite seu nome de usuário administrativo',
        col={"sm": 8, "md": 12, "xl": 12},
        on_change=generator_avatar,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
    )

    input_senha = ft.TextField(
        hint_text='Digite sua senha administrativa',
        password=True,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        can_reveal_password=True,
        col={"sm": 8, "md": 12, "xl": 12},
    )

    password_reset_btn = ft.TextButton(
        text='Recuperar senha',
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
        on_click=lambda _: page.go('/adminregister')
    )

    def handle_login(e):
        username = input_username.value
        password = input_senha.value

        # Validação dos campos de login
        is_valid, error_message = validate_login(username, password)
        if not is_valid:
            logger.warning(f"Falha na validação do login para {username}: {error_message}")
            page.snack_bar = ft.SnackBar(content=ft.Text(error_message,
                                                         size=20,
                                                         color=ft.colors.RED,
                                                         weight=ft.FontWeight.W_600,
                                                         italic=True
                                                         ))
            page.snack_bar.open = True
            page.update()
            return

        try:
            admin = Fetch.fetch_admin_by_username(username)

            if admin is not None:
                try:
                    encrypted_password = admin['password']
                    stored_password = decrypt(encrypted_password, SECRET_KEY)
                except Exception as ex:
                    logger.error(f"Erro ao descriptografar a senha para o Administrador {username}: {ex}")
                    page.snack_bar = ft.SnackBar(content=ft.Text("Erro na autenticação. Tente novamente.", size=20,
                                                                 color=ft.colors.RED,
                                                                 weight=ft.FontWeight.W_600,
                                                                 italic=True))
                    page.snack_bar.open = True
                    page.update()
                    return

                if stored_password == password:
                    # Login bem-sucedido, armazena sessão e redireciona para o painel do administrador
                    page.session.set("admin_id", admin['id'])
                    page.session.set("admin_username", admin['username'])
                    logger.info(f"Login bem-sucedido para admin: {username}, ID: {admin['id']}")

                    # Notifica o sucesso
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(f'Seja bem-vindo de volta, {username}! Pronto para continuar liderando?',
                                        size=20, color=ft.colors.BLUE, weight=ft.FontWeight.W_600)
                    )
                    page.snack_bar.open = True
                    page.update()

                    # Redireciona para o painel do administrador
                    page.go('/admin')
                else:
                    logger.warning(f"Senha incorreta para o admin {username}")
                    page.snack_bar = ft.SnackBar(content=ft.Text("Nome de usuário ou senha inválidos. Por favor, "
                                                                 "tente novamente."))
                    page.snack_bar.open = True
                    page.update()
            else:
                logger.warning(f"Administrador {username} não encontrado.")
                page.snack_bar = ft.SnackBar(content=ft.Text("Nome de usuário ou senha inválidos. Por favor, tente "
                                                             "novamente."))
                page.snack_bar.open = True
                page.update()

        except Exception as ex:
            logger.error(f"Erro ao efetuar login para o administrador {username}: {ex}")
            page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    value=f"Ocorreu um erro ao tentar acessar sua conta. Por favor, verifique suas credenciais e "
                          f"tente novamente.",
                    size=20,
                    color=ft.colors.RED,
                    weight=ft.FontWeight.W_600
                )
            )
            page.snack_bar.open = True
            page.update()

    # Layout da página de login de administrador
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
                                        controls=[avatar]
                                    ),
                                    ft.Text(
                                        value="Acesso Administrativo",
                                        size=20,
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.BOLD,
                                        overflow=ft.TextOverflow.ELLIPSIS,
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
                                controls=[password_reset_btn]
                            ),
                            ft.ElevatedButton(
                                text="Acessar painel",
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
                                on_click=handle_login
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[new_account_btn]
                            ),
                        ],
                        run_spacing={"xs": 10},
                    ),
                ],
                spacing=20
            )
        )
    )
