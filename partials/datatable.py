import flet as ft


class Data_tb(ft.UserControl):
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
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            col={"sm": 8, "md": 4, "xl": 8},
                            controls=[
                                ft.Text(value="Meus Usuários", size=32, weight=ft.FontWeight.W_900,
                                        color=ft.colors.WHITE),
                            ]
                        ),
                        ft.Column(
                            col={"sm": 6, "md": 4, "xl": 2},
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    spans=[
                                        ft.TextSpan(text='117'),
                                        ft.TextSpan(text='Registros'),
                                    ]
                                )
                            ]
                        ),
                        ft.Column(
                            col={"sm": 6, "md": 4, "xl": 2},
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value="3", size=32, weight=ft.FontWeight.W_700,
                                        color=ft.colors.WHITE),
                                ft.Text(value="Solicitações", size=16, color=ft.colors.GREY_50),
                            ]
                        ),
                        ft.Column(
                            col={"sm": 6, "md": 4, "xl": 2},
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value="90", size=32, weight=ft.FontWeight.W_700,
                                        color=ft.colors.WHITE),
                                ft.Text(value="Ativos", size=16, color=ft.colors.GREY_50),
                            ]
                        ),
                        ft.Divider(height=30),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Task")),
                                ft.DataColumn(ft.Text("Status")),
                                ft.DataColumn(ft.Text("Assigned To")),
                                ft.DataColumn(ft.Text("Due Date")),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Update website")),
                                        ft.DataCell(ft.Text("In progress")),
                                        ft.DataCell(ft.Text("Alice")),
                                        ft.DataCell(ft.Text("2024-09-10")),
                                    ],
                                ),
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Fix bugs in API")),
                                        ft.DataCell(ft.Text("Done")),
                                        ft.DataCell(ft.Text("John")),
                                        ft.DataCell(ft.Text("2024-09-12")),
                                    ],
                                ),
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Design new logo")),
                                        ft.DataCell(ft.Text("In progress")),
                                        ft.DataCell(ft.Text("Mary")),
                                        ft.DataCell(ft.Text("2024-09-15")),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
            )
        )
