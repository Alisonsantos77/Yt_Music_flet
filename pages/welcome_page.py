import flet as ft


def WelcomePage(page: ft.Page):
    def go_to_login_user(e):
        page.go("/login")

    def go_to_login_admin(e):
        page.go("/adminlogin")

    return ft.Container(
        padding=ft.padding.symmetric(horizontal=20, vertical=40),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value='AlDev',
                            size=30,
                            color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            value='Os melhores aplicativos para você!',
                            style=ft.TextStyle(
                                size=12,
                                weight=ft.FontWeight.W_500,
                                color=ft.colors.GREY_300,
                            ),
                        )
                    ]
                ),

                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Lottie(
                            src='https://lottie.host/f6664f89-2e9d-411d-a4e3-be21972e11c1/vBN4A9USVL.json',
                            repeat=True,
                            reverse=True,
                            animate=True,
                            background_loading=True,
                            filter_quality=ft.FilterQuality.HIGH,
                            fit=ft.ImageFit.CONTAIN,
                            col={"sm": 10, "xl": 12},
                            width=300,
                            height=300
                        )
                    ]
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            value="Quem é você hoje?",
                            style=ft.TextStyle(
                                size=18,
                                weight=ft.FontWeight.W_600,
                                color=ft.colors.WHITE,
                            ),
                            col={"sm": 10, "xl": 12},
                        ),
                    ]
                ),

                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            text='Usuário',
                            bgcolor=ft.colors.BLUE_800,
                            color=ft.colors.WHITE,
                            on_click=go_to_login_user,
                            col={"sm": 6, "md": 4},
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: ft.colors.BLUE_600,
                                    "": ft.colors.BLUE_800,
                                },
                                color=ft.colors.WHITE,
                                shape=ft.RoundedRectangleBorder(radius=6),
                                elevation=2
                            )
                        ),
                        ft.ElevatedButton(
                            text='Administrador',
                            color=ft.colors.BLUE_800,
                            on_click=go_to_login_admin,
                            col={"sm": 6, "md": 4},
                            style=ft.ButtonStyle(
                                color={
                                    ft.ControlState.HOVERED: ft.colors.BLUE_400,
                                    ft.ControlState.FOCUSED: ft.colors.BLUE,
                                    ft.ControlState.DEFAULT: ft.colors.BLUE_800,
                                },
                                bgcolor={ft.ControlState.FOCUSED: ft.colors.TRANSPARENT, "": ft.colors.BACKGROUND},
                                overlay_color=ft.colors.TRANSPARENT,
                                elevation={"pressed": 0, "": 1},
                                animation_duration=500,
                                side={
                                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.colors.BLUE),
                                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.colors.BLUE),
                                },
                                shape=ft.RoundedRectangleBorder(radius=6),
                            ),
                        ),
                    ]
                ),

                ft.Text(
                    value="© 2024 AlDev - Todos os direitos reservados",
                    size=10,
                    color=ft.colors.GREY_400,
                    weight=ft.FontWeight.W_400,
                    col={"sm": 10, "xl": 12},
                )
            ],
        )
    )
