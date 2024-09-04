import flet as ft
from utils.validations import validate_login
from services import Fetch, Commit


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
        border="underline",
        max_lines=1,
        max_length=20,
    )

    input_senha = ft.TextField(
        hint_text='Insira sua senha',
        password=True,
        border="underline",
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

        # Validando os campos de login
        is_valid, error_message = validate_login(username, password)
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

            if admin is not None:
                if admin['password'] == password:
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
            elif user is not None:
                if user['password'] == password:
                    # Atualizar o último login
                    Commit.update_last_login(user['id'])

                    # Verificar se o avatar do usuário está registrado
                    if 'avatar_url' not in user or not user['avatar_url']:
                        # Atualizar o avatar no perfil do usuário
                        avatar_url = new_avatar.current.foreground_image_src
                        Commit.update_avatar_url(user['id'], avatar_url)

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
