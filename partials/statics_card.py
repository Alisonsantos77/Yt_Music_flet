import flet as ft


class Card_statics(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expand = True

    def build(self):
        ft.Container(
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
