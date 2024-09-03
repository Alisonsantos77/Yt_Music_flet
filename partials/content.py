import flet as ft
from components.searchbar import SearchBarItem


class MainContent(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expand = True

    def build(self):
        searchbar = SearchBarItem(placeholder="Pesquisar...")

        header_dt = ft.Container(
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
                                ft.Text(value="117 registros", size=16,
                                        color=ft.colors.GREY_50)
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

        statics = ft.Container(
            image_src='https://images3.alphacoders.com/133/1332803.png',
            image_fit=ft.ImageFit.COVER,
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
                    col=6,
                    controls=[
                        ft.LineChart(
                            data_series=[
                                ft.LineChartData(
                                    data_points=[
                                        ft.LineChartDataPoint(1, 1),
                                        ft.LineChartDataPoint(3, 2.8),
                                        ft.LineChartDataPoint(7, 1.2),
                                        ft.LineChartDataPoint(10, 2.8),
                                        ft.LineChartDataPoint(12, 2.6),
                                        ft.LineChartDataPoint(13, 3.9),
                                    ],
                                    color=ft.colors.PINK,
                                    stroke_width=4,
                                    curved=True,
                                    stroke_cap_round=True,
                                ),
                                ft.LineChartData(
                                    data_points=[
                                        ft.LineChartDataPoint(1, 2.8),
                                        ft.LineChartDataPoint(3, 1.9),
                                        ft.LineChartDataPoint(6, 3),
                                        ft.LineChartDataPoint(10, 1.3),
                                        ft.LineChartDataPoint(13, 2.5),
                                    ],
                                    color=ft.colors.CYAN,
                                    stroke_width=4,
                                    curved=True,
                                    stroke_cap_round=True,
                                ),
                            ],
                            border=ft.Border(
                                bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE))
                            ),
                            left_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(value=1, label=ft.Text("1m", size=14, weight=ft.FontWeight.BOLD)),
                                    ft.ChartAxisLabel(value=2, label=ft.Text("2m", size=14, weight=ft.FontWeight.BOLD)),
                                    ft.ChartAxisLabel(value=3, label=ft.Text("3m", size=14, weight=ft.FontWeight.BOLD)),
                                ],
                                labels_size=40,
                            ),
                            bottom_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(value=2,
                                                      label=ft.Container(
                                                          ft.Text("SEP", size=16, weight=ft.FontWeight.BOLD))),
                                    ft.ChartAxisLabel(value=7,
                                                      label=ft.Container(
                                                          ft.Text("OCT", size=16, weight=ft.FontWeight.BOLD))),
                                    ft.ChartAxisLabel(value=12,
                                                      label=ft.Container(
                                                          ft.Text("DEC", size=16, weight=ft.FontWeight.BOLD))),
                                ],
                                labels_size=32,
                            ),
                            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
                            min_y=0,
                            max_y=4,
                            min_x=0,
                            max_x=14,
                            expand=True,
                        ),
                    ]
                )
            )
        )

        requests = ft.Container(
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
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.HIDDEN,
                        controls=[
                            searchbar,
                            header_dt,
                            statics,
                            requests,
                        ],
                        spacing=20,
                        expand=True,
                    )
                ],
                spacing=20,
                expand=True,
            ),
            bgcolor=ft.colors.BACKGROUND,
            padding=ft.padding.all(30)
        )
