import asyncio
import flet as ft
from components.searchbar import SearchBarItem
from services import Fetch, Commit
from datetime import datetime, timedelta, timezone


def calculate_active_users(users):
    active_threshold = datetime.now(timezone.utc) - timedelta(days=7)
    active_users = [user for user in users if datetime.fromisoformat(
        user['last_login']) >= active_threshold]
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
        self.filtered_users = Fetch.users  # Inicializa com todos os usuários
        self.table = None  # Inicializa a tabela
        self.table_container = None  # Inicializa o container da tabela
        self.requests_stack = None  # Inicializa requests_stack
        self.update_interval = 120  # Intervalo para verificação (em segundos)

    async def verify_requests(self):
        """Verifica continuamente as solicitações pendentes."""
        while True:
            Fetch.fetch_all_requests()
            self.update_requests_stack()  # Atualiza o requests_stack com as novas solicitações
            print(f"Verificação de novas solicitações às {datetime.now()}")
            # Intervalo entre verificações
            await asyncio.sleep(self.update_interval)

    def update_requests_stack(self):
        """Atualiza o requests_stack com as solicitações mais recentes, ordenando da mais recente para a mais antiga."""
        sorted_requests = sorted(
            Fetch.requests, key=lambda x: x['created_at'], reverse=True)

        self.requests_stack.controls = [
            ft.Dismissible(
                content=ft.Container(
                    padding=ft.padding.all(20),
                    border_radius=ft.border_radius.all(10),
                    bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
                    blur=ft.Blur(sigma_x=8, sigma_y=8),
                    shadow=ft.BoxShadow(
                        blur_radius=50, color=ft.colors.BLACK12),
                    border=ft.Border(
                        top=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                        right=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                    ),
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
                                                            content=ft.Text(
                                                                request['username'][0:1].upper()),
                                                            width=100,
                                                        ),
                                                        ft.Container(
                                                            content=ft.Text(
                                                                value=request['username'],
                                                                size=24,
                                                                color=ft.colors.WHITE,
                                                                weight=ft.FontWeight.BOLD,
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
                                                                    ft.Icon(
                                                                        name=ft.icons.EMAIL),
                                                                    ft.Text(
                                                                        value=request['email'],
                                                                        size=16,
                                                                        color=ft.colors.WHITE,
                                                                        weight=ft.FontWeight.BOLD,
                                                                    ),
                                                                ]
                                                            ),
                                                            col={"xs": 12, "sm": 6, "md": 5, "lg": 6, "xl": 12,
                                                                 "xxl": 6},
                                                        ),
                                                        ft.Container(
                                                            content=ft.Row(
                                                                controls=[
                                                                    ft.Icon(
                                                                        name=ft.icons.CALENDAR_TODAY),
                                                                    ft.Text(
                                                                        value=datetime.fromisoformat(
                                                                            request['created_at']).strftime(
                                                                            "%Y-%m-%d"),
                                                                        size=16,
                                                                        color=ft.colors.WHITE,
                                                                        weight=ft.FontWeight.BOLD,
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
                                            on_click=lambda e, req_id=request['id']: self.page.run_task(
                                                self.reject_request, req_id, self.page.session.get(
                                                    "admin_id")
                                                # Recuperando o admin_id da sessão
                                            ),
                                        ),
                                        ft.ElevatedButton(
                                            text='Aceitar',
                                            bgcolor=ft.colors.GREEN,
                                            color=ft.colors.WHITE,
                                            on_click=lambda e, req_id=request['id']: self.page.run_task(
                                                self.accept_request, req_id, self.page.session.get(
                                                    "admin_id")
                                                # Recuperando o admin_id da sessão
                                            ),
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
                    animate=ft.Animation(
                        duration=200, curve=ft.AnimationCurve.DECELERATE),
                    animate_offset=True,
                    animate_scale=True,
                    animate_opacity=True,
                ),
                data=pos,
                dismiss_direction=ft.DismissDirection.HORIZONTAL,
                on_dismiss=self.handle_dismiss,
                on_update=self.handle_update,
                on_confirm_dismiss=self.handle_confirm_dismiss,
            ) for pos, request in reversed(list(enumerate(sorted_requests)))
        ]

        self.requests_stack.update()

    async def accept_request(self, request_id, admin_id):
        request = next(
            (req for req in Fetch.requests if req['id'] == request_id), None)
        if request:
            user_data = {
                'username': request['username'],
                'email': request['email'],
                'password': request['password'],
                # 'created_at': request['created_at'],
                'approved_by_admin_id': admin_id
            }
            try:
                Commit.update_request_with_admin(request_id, admin_id)
                await asyncio.sleep(3)
                Commit.commit_user_to_table(user_data)
                await asyncio.sleep(5)
                Commit.remove_request_from_registration(request_id)

                Fetch.fetch_all_users()
                Fetch.fetch_all_requests()

                self.update_requests_stack()
                self.requests_stack.update()

                self.update_table(None)
                self.table.update()
            except Exception as error:
                print(f"Erro ao aceitar request {request_id}: {error}")
        else:
            print(f"Request {request_id} não encontrada.")

    async def reject_request(self, request_id, admin_id):
        try:
            Commit.update_request_with_admin(request_id, admin_id)
            await asyncio.sleep(3)
            Commit.remove_request_from_registration(request_id)
            await asyncio.sleep(3)
            Fetch.fetch_all_requests()

            self.update_requests_stack()
            self.requests_stack.update()

            self.update_table(None)  # Atualiza a tabela de usuários
            self.table.update()

            print(f"Request {request_id} foi rejeitada e removida da lista.")
        except Exception as error:
            print(f"Erro ao rejeitar request {request_id}: {error}")

    def handle_dismiss(self, e):
        request_index = e.control.data
        del Fetch.requests[request_index]
        self.requests_stack.controls.pop()
        e.page.update()
        self.page.update()

    def handle_update(self, e: ft.DismissibleUpdateEvent):
        print(
            f"Update - direction: {e.direction}, reached: {e.reached}, previous_reached: {e.previous_reached}")

    def handle_confirm_dismiss(self, e: ft.DismissibleDismissEvent):
        if e.direction == ft.DismissDirection.END_TO_START:
            e.control.scale = ft.Scale(scale=1.2)
            self.page.update()
            e.control.confirm_dismiss(True)
        else:
            e.control.confirm_dismiss(True)

    def update_table(self, search_results):
        if search_results:
            self.filtered_users = search_results
        else:
            self.filtered_users = Fetch.users

        self.table.rows = [
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
                        datetime.fromisoformat(user['created_at']).strftime(
                            "%d-%m-%Y %H:%M:%S")
                    )),
                    ft.DataCell(ft.Text(
                        datetime.fromisoformat(user['last_login']).strftime(
                            "%d-%m-%Y %H:%M:%S")
                    )),
                ],
            ) for user in self.filtered_users
        ]
        self.update()

    def build(self):
        self.filtered_users = Fetch.users
        self.table = None

        searchbar = SearchBarItem(on_search_results=self.update_table)

        self.table = ft.DataTable(
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
                            datetime.fromisoformat(user['created_at']).strftime(
                                "%d-%m-%Y %H:%M:%S")
                        )),
                        ft.DataCell(ft.Text(
                            datetime.fromisoformat(user['last_login']).strftime(
                                "%d-%m-%Y %H:%M:%S")
                        )),
                    ],
                ) for user in self.filtered_users
            ],
        )

        self.table_container = ft.Container(
            expand=True,
            content=self.table,
            padding=ft.padding.symmetric(vertical=50, horizontal=80),
            border_radius=ft.border_radius.all(10),
            blur=ft.Blur(sigma_x=8, sigma_y=8),
            bgcolor=ft.colors.with_opacity(0.1, ft.colors.WHITE),
            border=ft.Border(
                top=ft.BorderSide(width=2, color=ft.colors.WHITE30),
                right=ft.BorderSide(width=2, color=ft.colors.WHITE30),
            ),
        )

        self.requests_stack = ft.Stack(
            controls=[]  # Será populado depois
        )

        self.page.run_task(self.verify_requests)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        scroll=ft.ScrollMode.HIDDEN,
                        controls=[
                            searchbar,
                            self.table_container,
                            ft.ResponsiveRow(
                                controls=[
                                    ft.Container(
                                        col={"sm": 12, "md": 5, "xl": 6},
                                        content=self.requests_stack
                                    )
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
