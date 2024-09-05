import flet as ft


class Card_requests(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expand = True

    def build(self):
        ft.Container(
            expand=True,
            alignment=ft.alignment.center,
            content=ft.Container(
                padding=ft.padding.symmetric(vertical=50, horizontal=80),
                border_radius=ft.border_radius.all(10),
                blur=ft.Blur(sigma_x=8, sigma_y=8),
                bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                border=ft.Border(
                    top=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                    right=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                ),
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Stack(
                            controls=[
                                ft.Dismissible(
                                    content=ft.Container(
                                        width=300,
                                        padding=ft.padding.all(20),
                                        border_radius=ft.border_radius.all(15),
                                        bgcolor=ft.colors.WHITE,
                                        content=ft.Column(
                                            controls=[
                                                ft.ResponsiveRow(
                                                    [

                                                        ft.CircleAvatar(
                                                            col={"sm": 6, "md": 4, "xl": 2},
                                                            foreground_image_src="https://randomuser.me/api"
                                                                                 "/portraits/men/5.jpg",
                                                            content=ft.Text("FF"),
                                                        ),

                                                        ft.Container(
                                                            ft.Text("Column 2"),
                                                            padding=5,
                                                            bgcolor=ft.colors.GREEN,
                                                            col={"sm": 6, "md": 4, "xl": 2},
                                                        ),
                                                        ft.Container(
                                                            ft.Text("Column 3"),
                                                            padding=5,
                                                            bgcolor=ft.colors.BLUE,
                                                            col={"sm": 6, "md": 4, "xl": 2},
                                                        ),
                                                        ft.Container(
                                                            ft.Text("Column 4"),
                                                            padding=5,
                                                            bgcolor=ft.colors.PINK_300,
                                                            col={"sm": 6, "md": 4, "xl": 2},
                                                        ),
                                                    ],
                                                ),
                                                ft.Row(
                                                    controls=[
                                                        ft.ElevatedButton(
                                                            text='Rejeitar',
                                                            bgcolor=ft.colors.RED
                                                        ),
                                                        ft.ElevatedButton(
                                                            text='Aceitar',
                                                            color='white',
                                                            bgcolor=ft.colors.PRIMARY
                                                        ),
                                                    ],
                                                    spacing=10,
                                                    alignment=ft.MainAxisAlignment.START,
                                                ),
                                            ]
                                        ),
                                    ),
                                    dismiss_direction=ft.DismissDirection.HORIZONTAL,
                                    background=ft.Container(bgcolor=ft.colors.LIGHT_BLUE_50),
                                    secondary_background=ft.Container(bgcolor=ft.colors.RED_ACCENT),
                                    on_dismiss=lambda e: print("Item dismissed"),
                                ),
                                ft.Container(
                                    width=60,
                                    height=60,
                                    alignment=ft.alignment.center,
                                    border_radius=ft.border_radius.all(30),
                                    bgcolor=ft.colors.GREY_300,
                                    content=ft.Icon(name=ft.icons.ARROW_FORWARD_IOS, size=20),
                                    right=0,
                                    margin=ft.margin.only(right=10),
                                ),
                            ]
                        ),
                    ]
                )
            )
        )
