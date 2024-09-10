import flet as ft
from utils.validations import validate_register
from services import Commit, Fetch
from flet.security import encrypt
from config import SECRET_KEY
from loguru import logger


def AdminRegisterPage(page: ft.Page):
    new_avatar = ft.Ref[ft.CircleAvatar]()

    def generator_avatar(e):
        if not input_username.value:
            new_avatar.current.foreground_image_src = "https://robohash.org/admindefault.png"
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
        col={"sm": 5, "md": 4, "xl": 8},
    )

    def login_redirect(e):
        page.go('/login')

    input_username = ft.TextField(
        hint_text='Nome de usuário (Admin)',
        col={"sm": 12, "md": 10, "xl": 8},
        on_change=generator_avatar,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        error_text=None
    )

    input_email = ft.TextField(
        hint_text='E-mail',
        col={"sm": 12, "md": 10, "xl": 8},
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=50,
        error_text=None
    )

    input_senha = ft.TextField(
        hint_text='Senha',
        password=True,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        can_reveal_password=True,
        col={"sm": 12, "md": 10, "xl": 8},
        error_text=None
    )

    input_senha_confirm = ft.TextField(
        hint_text='Confirmar senha',
        password=True,
        border=ft.InputBorder.UNDERLINE,
        max_lines=1,
        max_length=20,
        can_reveal_password=True,
        col={"sm": 12, "md": 10, "xl": 8},
        error_text=None
    )

    def validate_password_strength(e):
        pwd_value = input_senha.value
        if len(pwd_value) < 8:
            input_senha.error_text = "A senha deve ter no mínimo 8 caracteres."
            input_senha.color = ft.colors.RED
        elif any(not c.isalnum() for c in pwd_value):
            input_senha.error_text = "Senha forte."
            input_senha.color = ft.colors.GREEN
        else:
            input_senha.error_text = "Senha média. Considere adicionar caracteres especiais."
            input_senha.color = ft.colors.ORANGE
        input_senha.update()

    input_senha.on_change = validate_password_strength

    have_account = ft.TextButton(
        text='Já possui uma conta?',
        col=12,
        style=ft.ButtonStyle(
            color={
                ft.ControlState.DEFAULT: ft.colors.WHITE,
                ft.ControlState.HOVERED: ft.colors.BLACK,
            },
            elevation=2,
            overlay_color=ft.colors.TRANSPARENT,

        ),
        on_click=login_redirect
    )

    def handle_register(e):
        username = input_username.value.strip()
        email = input_email.value.strip()
        password = input_senha.value.strip()
        confirm_password = input_senha_confirm.value.strip()

        # Validação de senha e campos com o validate_register
        is_valid, error_message = validate_register(username, email, password, confirm_password)
        if not is_valid:
            if "nome de usuário" in error_message:
                input_username.error_text = error_message
                input_username.update()
            elif "email" in error_message:
                input_email.error_text = error_message
                input_email.update()
            elif "senha" in error_message:
                input_senha.error_text = error_message
                input_senha.update()
            elif "senhas não correspondem" in error_message:
                input_senha_confirm.error_text = error_message
                input_senha_confirm.update()
            return

        # Verifica se o username ou email já existe na base de admins ou users
        existing_user_or_email = Fetch.fetch_user_or_admin_by_username(username) or Fetch.fetch_user_or_admin_by_email(
            email)
        if existing_user_or_email:
            input_username.error_text = "Usuário ou e-mail já existe."
            input_username.update()
            return

        try:
            encrypted_password = encrypt(password, SECRET_KEY)
            avatar_url = f"https://robohash.org/{username}.png"

            # Cria o novo admin
            Commit.commit_admin_to_table(
                data={
                    'username': username,
                    'email': email,
                    'password': encrypted_password,
                    'avatar_url': avatar_url,
                }
            )

            page.snack_bar = ft.SnackBar(content=ft.Text("Administrador cadastrado com sucesso!",
                                                         size=20,
                                                         color=ft.colors.BLUE,
                                                         weight=ft.FontWeight.W_600,
                                                         italic=True
                                                         ))
            page.snack_bar.open = True
            page.update()
            page.go('/login')

        except Exception as error:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao cadastrar administrador: {str(error)}",
                                                         size=20,
                                                         color=ft.colors.RED,
                                                         weight=ft.FontWeight.W_600,
                                                         italic=True
                                                         ))
            page.snack_bar.open = True
            page.update()

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Container(
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            border_radius=ft.border_radius.all(10),
            blur=ft.Blur(sigma_x=8, sigma_y=8),
            margin=5,
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            border=ft.Border(
                top=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                right=ft.BorderSide(width=2, color=ft.colors.WHITE30),
            ),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
                                        value="Junte-se à nossa equipe de líderes",
                                        size=20,
                                        color=ft.colors.WHITE,
                                        weight=ft.FontWeight.BOLD,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                        col={"sm": 5, "md": 4, "xl": 12},
                                    ),
                                    ft.Text(
                                        value="Crie sua conta de administrador e lidere a inovação na Aldev.",
                                        size=14,
                                        color=ft.colors.GREY_50,
                                        weight=ft.FontWeight.W_600,
                                        overflow=ft.TextOverflow.ELLIPSIS,
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
                            input_email,
                            input_senha,
                            input_senha_confirm,
                            ft.ElevatedButton(
                                text="Registrar Admin",
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
                                on_click=handle_register,
                                col={"sm": 8, "md": 10, "xl": 6},
                            ),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    have_account
                                ]
                            ),
                        ],
                        run_spacing={"xs": 5},
                    ),
                ],
                spacing=5
            )
        )
    )
