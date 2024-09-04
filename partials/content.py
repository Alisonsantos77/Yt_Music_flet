import flet as ft
from components.searchbar import SearchBarItem
from services import Fetch, Commit
from datetime import datetime, timedelta, timezone


def calculate_active_users(users):
    active_threshold = datetime.now(timezone.utc) - timedelta(days=7)
    active_users = [user for user in users if datetime.fromisoformat(user['last_login']) >= active_threshold]
    return len(active_users)


def group_users_by_month(users):
    grouped_users = {}
    for user in users:
        month = datetime.fromisoformat(user['created_at']).strftime("%Y-%m")
        if month not in grouped_users:
            grouped_users[month] = 0
        grouped_users[month] += 1
    return grouped_users


Fetch.fetch_all_users()
quantity_active_users = calculate_active_users(Fetch.users)
quantity_users = len(Fetch.users)

Fetch.fetch_all_requests()
quantity_requests = len(Fetch.requests)

users_by_month = group_users_by_month(Fetch.users)


class MainContent(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expand = True

    def build(self):
        searchbar = SearchBarItem(placeholder="Pesquisar...")

        def accept_request(request_id):
            # Encontrar a request correspondente no Fetch.requests
            request = next((req for req in Fetch.requests if req['id'] == request_id), None)

            if request:
                # Simulação de aceitar a request, como mover para tabela de usuários
                user_data = {
                    'username': request['username'],
                    'email': request['email'],
                    'password': request['password'],
                    'created_at': datetime.now(timezone.utc).isoformat(),
                }

                # Enviar os dados para a tabela de usuários no backend
                try:
                    Commit.commit_user_to_table(user_data)  # Função que move para a tabela de usuários
                    print(f"Usuário {user_data['username']} aceito e movido para a tabela de usuários.")

                    # Remover request da tabela registration_requests
                    Commit.remove_request_from_registration(request_id)

                    Fetch.fetch_all_users()

                    # Após aceitar, remover a request da lista Fetch.requests localmente
                    Fetch.requests = [req for req in Fetch.requests if req['id'] != request_id]
                    print(f"Request {request_id} foi aceita e removida da lista local.")

                    self.page.update()
                except Exception as error:
                    print(f"Erro ao aceitar request {request_id}: {error}")
            else:
                print(f"Request {request_id} não encontrada.")

        def handle_dismiss(e):
            # Remove o item da lista e atualiza a pilha
            request_index = e.control.data
            del Fetch.requests[request_index]
            requests_stack.controls.pop()
            e.page.update()
            self.page.update()

        def handle_update(e: ft.DismissibleUpdateEvent):
            # Função chamada quando o item é arrastado (update visual durante o movimento)
            print(
                f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}")

        def handle_confirm_dismiss(e: ft.DismissibleDismissEvent):
            # Função para confirmar o deslize e aplicar o efeito de escala e animação de retorno
            if e.direction == ft.DismissDirection.END_TO_START:  # deslize para direita-esquerda
                e.control.scale = ft.Scale(scale=1.2)  # Aumenta a escala
                self.page.update()
                e.control.confirm_dismiss(True)  # Confirma o deslize
            else:
                e.control.confirm_dismiss(True)  # Deslize aceito sem confirmação adicional

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
                            col={"sm": 8, "md": 4, "xl": 6},
                            controls=[
                                ft.Text(value="Meus Usuários", size=32, weight=ft.FontWeight.W_900,
                                        color=ft.colors.WHITE),
                            ]
                        ),
                        ft.Column(
                            col={"sm": 6, "md": 4, "xl": 2},
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value=str(quantity_users), size=32, weight=ft.FontWeight.W_700,
                                        color=ft.colors.WHITE),
                                ft.Text(value="Registros", size=16, color=ft.colors.GREY_50),
                            ]
                        ),
                        ft.Column(
                            col={"sm": 6, "md": 4, "xl": 2},
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value=str(quantity_requests), size=32, weight=ft.FontWeight.W_700,
                                        color=ft.colors.WHITE),
                                ft.Text(value="Solicitações", size=16, color=ft.colors.GREY_50),
                            ]
                        ),
                        ft.Column(
                            col={"sm": 6, "md": 4, "xl": 2},
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value=str(quantity_active_users), size=32, weight=ft.FontWeight.W_700,
                                        color=ft.colors.WHITE),
                                ft.Text(value="Ativos", size=16, color=ft.colors.GREY_50),
                            ]
                        ),
                        ft.Divider(height=30),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Avatar")),
                                ft.DataColumn(ft.Text("Username")),
                                ft.DataColumn(ft.Text("Email")),
                                ft.DataColumn(ft.Text("Created At")),
                                ft.DataColumn(ft.Text("Last Login")),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(
                                            ft.CircleAvatar(
                                                foreground_image_src=user['avatar_url'] if user[
                                                    'avatar_url'] else "https://robohash.org/userdefault.png",
                                                content=ft.Text(user['username'][0:1].upper()),
                                            )
                                        ),
                                        ft.DataCell(ft.Text(user['username'])),
                                        ft.DataCell(ft.Text(user['email'])),
                                        ft.DataCell(ft.Text(
                                            datetime.fromisoformat(user['created_at']).strftime("%Y-%m-%d %H:%M:%S"))),
                                        ft.DataCell(ft.Text(
                                            datetime.fromisoformat(user['last_login']).strftime("%Y-%m-%d %H:%M:%S"))),
                                    ],
                                ) for user in Fetch.users
                            ],
                        )
                    ],
                ),
            )
        )

        statics = ft.Container(
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
                        ft.LineChart(
                            data_series=[
                                ft.LineChartData(
                                    data_points=[
                                        ft.LineChartDataPoint(1, users_by_month.get("2024-01", 0)),
                                        ft.LineChartDataPoint(2, users_by_month.get("2024-02", 0)),
                                        ft.LineChartDataPoint(3, users_by_month.get("2024-03", 0)),
                                        ft.LineChartDataPoint(4, users_by_month.get("2024-04", 0)),
                                        ft.LineChartDataPoint(5, users_by_month.get("2024-05", 0)),
                                        ft.LineChartDataPoint(6, users_by_month.get("2024-06", 0)),
                                    ],
                                    color=ft.colors.PINK,
                                    stroke_width=4,
                                    curved=True,
                                    stroke_cap_round=True,
                                ),
                                ft.LineChartData(
                                    data_points=[
                                        ft.LineChartDataPoint(1, users_by_month.get("2024-01", 0)),
                                        ft.LineChartDataPoint(2, users_by_month.get("2024-02", 0)),
                                        ft.LineChartDataPoint(3, users_by_month.get("2024-03", 0)),
                                        ft.LineChartDataPoint(4, users_by_month.get("2024-04", 0)),
                                        ft.LineChartDataPoint(5, users_by_month.get("2024-05", 0)),
                                        ft.LineChartDataPoint(6, users_by_month.get("2024-06", 0)),
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
                                    ft.ChartAxisLabel(value=1,
                                                      label=ft.Text("Jan", size=14, weight=ft.FontWeight.BOLD)),
                                    ft.ChartAxisLabel(value=2,
                                                      label=ft.Text("Feb", size=14, weight=ft.FontWeight.BOLD)),
                                    ft.ChartAxisLabel(value=3,
                                                      label=ft.Text("Mar", size=14, weight=ft.FontWeight.BOLD)),
                                    ft.ChartAxisLabel(value=4,
                                                      label=ft.Text("Apr", size=14, weight=ft.FontWeight.BOLD)),
                                    ft.ChartAxisLabel(value=5,
                                                      label=ft.Text("May", size=14, weight=ft.FontWeight.BOLD)),
                                    ft.ChartAxisLabel(value=6,
                                                      label=ft.Text("Jun", size=14, weight=ft.FontWeight.BOLD)),
                                ],
                                labels_size=40,
                            ),
                            bottom_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(value=1,
                                                      label=ft.Container(
                                                          ft.Text("2024", size=16, weight=ft.FontWeight.BOLD))),
                                    ft.ChartAxisLabel(value=6,
                                                      label=ft.Container(
                                                          ft.Text("2025", size=16, weight=ft.FontWeight.BOLD))),
                                ],
                                labels_size=32,
                            ),
                            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
                            min_y=0,
                            max_y=10,
                            min_x=1,
                            max_x=6,
                            expand=True,
                        ),
                    ]
                )
            )
        )

        requests_stack = ft.Stack(
            controls=[
                ft.Dismissible(
                    content=ft.Container(
                        padding=ft.padding.all(20),
                        border_radius=ft.border_radius.all(15),
                        bgcolor=ft.colors.WHITE,
                        shadow=ft.BoxShadow(blur_radius=50, color=ft.colors.BLACK12),
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    height=300,
                                    content=ft.ResponsiveRow(
                                        controls=[
                                            ft.Column(
                                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                                controls=[
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.CircleAvatar(
                                                                col={"xs": 12, "sm": 6, "md": 4, "lg": 3, "xl": 2,
                                                                     "xxl": 6},
                                                                foreground_image_src=request['avatar_url'] if request[
                                                                    'avatar_url'] else "https://robohash.org/userdefault.png",
                                                                content=ft.Text(request['username'][0:1].upper()),
                                                            ),
                                                            ft.Container(
                                                                content=ft.Text(
                                                                    value=request['username'],
                                                                    size=16,
                                                                    color=ft.colors.BLACK,
                                                                    weight=ft.FontWeight.W_600,
                                                                ),
                                                                col={"xs": 12, "sm": 6, "md": 5, "lg": 6, "xl": 6,
                                                                     "xxl": 6},
                                                            ),
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.Container(
                                                                content=ft.Row(
                                                                    controls=[
                                                                        ft.Icon(name=ft.icons.EMAIL),
                                                                        ft.Text(
                                                                            value=request['email'],
                                                                            size=16,
                                                                            color=ft.colors.BLACK,
                                                                            weight=ft.FontWeight.W_600,
                                                                        ),
                                                                    ]
                                                                ),
                                                                col={"xs": 12, "sm": 6, "md": 5, "lg": 6, "xl": 12,
                                                                     "xxl": 6},
                                                            ),
                                                            ft.Container(
                                                                content=ft.Row(
                                                                    controls=[
                                                                        ft.Icon(name=ft.icons.CALENDAR_TODAY),
                                                                        ft.Text(
                                                                            value=datetime.fromisoformat(
                                                                                request['created_at']).strftime(
                                                                                "%Y-%m-%d"),
                                                                            size=16,
                                                                            color=ft.colors.BLACK,
                                                                            weight=ft.FontWeight.W_600,
                                                                        ),
                                                                    ]
                                                                ),
                                                                col={"xs": 12, "sm": 6, "md": 5, "lg": 6, "xl": 6,
                                                                     "xxl": 6},
                                                            ),
                                                        ],
                                                        spacing=50
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                text='Rejeitar',
                                                bgcolor=ft.colors.RED,
                                                color=ft.colors.WHITE,
                                            ),
                                            ft.ElevatedButton(
                                                text='Aceitar',
                                                bgcolor=ft.colors.GREEN,
                                                color=ft.colors.WHITE,
                                                on_click=lambda e, req_id=request['id']: accept_request(req_id),
                                            ),

                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                        spacing=10,
                                    )
                                ),
                            ]
                        ),
                        offset=ft.Offset(x=0, y=0),
                        scale=ft.Scale(scale=1),
                        opacity=1,
                        animate=ft.Animation(duration=200, curve=ft.AnimationCurve.DECELERATE),
                        animate_offset=True,
                        animate_scale=True,
                        animate_opacity=True,
                    ),
                    data=pos,
                    dismiss_direction=ft.DismissDirection.HORIZONTAL,
                    on_dismiss=handle_dismiss,
                    on_update=handle_update,
                    on_confirm_dismiss=handle_confirm_dismiss,
                ) for pos, request in reversed(list(enumerate(Fetch.requests)))
            ]
        )
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.HIDDEN,
                        controls=[
                            header_dt,
                            ft.ResponsiveRow(
                                controls=[
                                    ft.Container(
                                        col={"sm": 12, "md": 5, "xl": 6},
                                        content=statics
                                    ),
                                    ft.Container(
                                        col={"sm": 12, "md": 5, "xl": 6},
                                        content=requests_stack
                                    ),
                                ]
                            )
                        ],
                        spacing=20,
                        expand=True,
                    ),
                ],
                spacing=20,
            ),
            bgcolor=ft.colors.BACKGROUND,
            padding=ft.padding.all(30)
        )
