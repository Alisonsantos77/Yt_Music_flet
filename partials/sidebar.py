import flet as ft


class SidebarHeader(ft.UserControl):

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.ResponsiveRow([
                        ft.Column(
                            col={"sm": 0, "xl": 4},
                            controls=[
                                ft.CircleAvatar(
                                    foreground_image_src="https://robohash.org/mail@ashallendesign.co.uk/portraits/men/3.jpg",
                                    width=100,
                                    height=100,
                                    content=ft.Text("AS"),
                                )
                            ]),
                        ft.Column(
                            col={"sm": 12, "xl": 8},
                            controls=[
                                ft.Text(value='Alison Santos', theme_style=ft.TextThemeStyle.BODY_LARGE),
                                ft.Text(value='Desenvolvedor Backend', theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                            ]
                        ),
                    ])
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=ft.padding.symmetric(vertical=20, horizontal=40),
            alignment=ft.alignment.center
        )


class SidebarContent(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.expand = True

    def logout_app(self, e):
        # Limpa a sessão ao fazer logout
        self.page.session.clear()
        self.page.snack_bar = ft.SnackBar(content=ft.Text("Você foi desconectado com sucesso!"))
        self.page.snack_bar.open = True
        self.page.update()

        # Redirecionar para a página de login
        self.page.go('/login')

    def build(self):
        menuitem = ft.Column(
            scroll=ft.ScrollMode.HIDDEN,
            controls=[
                ft.ListTile(
                    leading=ft.Icon(name=ft.icons.DASHBOARD),
                    title=ft.Text(value='Dashboard', theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                    on_click=lambda e: print("Dashboard clicked"),
                ),
                ft.ListTile(
                    leading=ft.Icon(name=ft.icons.WORK),
                    title=ft.Text(value='Projects', theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                    on_click=lambda e: print("Projects clicked"),
                ),
                ft.ListTile(
                    leading=ft.Icon(name=ft.icons.CHECKLIST),
                    title=ft.Text(value='Task list', theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                    selected=True,
                    hover_color=ft.colors.PRIMARY,
                    selected_color=ft.colors.ON_PRIMARY,
                    on_click=lambda e: print("Task list clicked"),
                ),
                ft.ListTile(
                    leading=ft.Icon(name=ft.icons.BUILD),
                    title=ft.Text(value='Services', theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                    on_click=lambda e: print("Services clicked"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            spacing=10,
        )
        logout = ft.ElevatedButton(
            icon=ft.icons.EXIT_TO_APP,
            text='Logout',
            color='red',
            on_click=self.logout_app
        )
        cv = ft.TextButton(
            text='Download CV', style=ft.ButtonStyle(color=ft.colors.GREY), icon=ft.icons.DOWNLOAD,
            icon_color=ft.colors.GREY,
            url='https://drive.google.com/uc?export=download&id=19UKY95n4gwQgweM5b6yiTt5N7B_u03Fj')

        return ft.Container(
            padding=ft.padding.all(20),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                scroll=ft.ScrollMode.HIDDEN,
                controls=[
                    ft.Divider(height=30),
                    menuitem,
                    ft.Divider(height=30),
                    logout,
                ]
            )
        )


class SidebarFooter(ft.UserControl):
    def build(self):
        return ft.Container(
            padding=ft.padding.symmetric(vertical=10),
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        content=ft.Image(src='icons/001-instagram.png', height=15, color='white'),
                        url='https://www.instagram.com/alisonsantos.eu/'
                    ),
                    ft.IconButton(
                        content=ft.Image(src='icons/002-linkedin.png', height=15, color='white'),
                        url='www.linkedin.com/in/alisonsantosdev'
                    ),
                    ft.IconButton(
                        content=ft.Image(src='icons/003-github.png', height=15, color='white'),
                        url='https://github.com/Alisonsantos77'
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )
        )


class Sidebar(ft.UserControl):
    def build(self):
        return ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    SidebarHeader(),
                    SidebarContent(),
                    SidebarFooter(),
                ]
            ),
            bgcolor=ft.colors.BACKGROUND
        )
