import requests
from config import URL, KEY


class Fetch:
    users = []
    admins = []
    requests = []

    @staticmethod
    def fetch_all_users():
        url = f'{URL}/rest/v1/User?select=*'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}"
        }
        res = requests.get(url, headers=headers)
        Fetch.users = res.json()

    @staticmethod
    def fetch_user_by_username(username):
        url = f'{URL}/rest/v1/User?username=eq.{username}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}"
        }
        res = requests.get(url, headers=headers)

        print(f"Status da resposta: {res.status_code}")
        #print(f"Conteúdo da resposta: {res.text}")

        if res.status_code == 200 and len(res.json()) > 0:
            return res.json()[0]
        return None

    @staticmethod
    def fetch_all_admins():
        url = f'{URL}/rest/v1/admins?select=*'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}"
        }
        res = requests.get(url, headers=headers)
        Fetch.admins = res.json()
        print(f"Status da resposta (admins): {res.status_code}")
        #print(f"Conteúdo da resposta (admins): {res.text}")

    @staticmethod
    def fetch_all_requests():
        url = f'{URL}/rest/v1/registration_requests?select=*'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}"
        }
        res = requests.get(url, headers=headers)
        Fetch.requests = res.json()
        print(f"Status da resposta (requests): {res.status_code}")
        #print(f"Conteúdo da resposta (requests): {res.text}")

    @staticmethod
    def fetch_admin_by_username(username):
        url = f'{URL}/rest/v1/admins?username=eq.{username}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}"
        }
        res = requests.get(url, headers=headers)

        print(f"Status da resposta (admin): {res.status_code}")
        #print(f"Conteúdo da resposta (admin): {res.text}")

        if res.status_code == 200 and len(res.json()) > 0:
            return res.json()[0]
        return None

    @staticmethod
    def fetch_and_update_user_table():
        # Atualizar a lista de usuários
        Fetch.fetch_all_users()  # Atualiza a lista de usuários no serviço Fetch
        print("Tabela de usuários foi atualizada.")


class Commit:
    @staticmethod
    def commit_user_to_table(data):
        url = f'{URL}/rest/v1/User'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        res = requests.post(url, headers=headers, json=data)
        print(res.status_code)
        #print(res.text)

    @staticmethod
    def commit_registration_request(data):
        url = f'{URL}/rest/v1/registration_requests'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        res = requests.post(url, headers=headers, json=data)
        print(res.status_code)
        #print(res.text)

    @staticmethod
    def update_last_login(user_id):
        url = f'{URL}/rest/v1/User?id=eq.{user_id}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        data = {
            'last_login': 'now()'
        }
        res = requests.patch(url, headers=headers, json=data)
        return res.status_code == 200

    @staticmethod
    def update_avatar_url(user_id, avatar_url):
        url = f'{URL}/rest/v1/User?id=eq.{user_id}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        data = {
            'avatar_url': avatar_url
        }
        res = requests.patch(url, headers=headers, json=data)
        if res.status_code == 200:
            print("Avatar atualizado com sucesso!")
        else:
            print(f"Erro ao atualizar avatar: {res.status_code}, {res.text}")

    @staticmethod
    def update_user_in_table(user_id, updated_data):
        url = f'{URL}/rest/v1/User?id=eq.{user_id}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        res = requests.patch(url, headers=headers, json=updated_data)
        if res.status_code == 200:
            print(f"Usuário {user_id} atualizado com sucesso.")
        else:
            print(f"Erro ao atualizar usuário {user_id}: {res.status_code}, {res.text}")

    def remove_request_from_registration(request_id):
        # URL para deletar uma request pelo ID
        url = f'{URL}/rest/v1/registration_requests?id=eq.{request_id}'

        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json',
        }

        # Realizar a requisição DELETE para remover a request
        res = requests.delete(url, headers=headers)

        if res.status_code == 200:
            print(f"Request {request_id} foi removida da tabela registration_requests.")
        else:
            print(f"Erro ao remover request {request_id}: {res.status_code}, {res.text}")

    def update_request_with_admin(request_id, admin_id):
        # URL para atualizar a request com o campo reviewed_by_admin_id
        url = f'{URL}/rest/v1/registration_requests?id=eq.{request_id}'

        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json',
        }

        # Dados para atualização: atribuir o admin_id e mudar o status para "accepted"
        update_data = {
            'reviewed_by_admin_id': admin_id,
            'status': 'accepted'
        }

        # Realizar a requisição PATCH para atualizar a request
        res = requests.patch(url, headers=headers, json=update_data)

        if res.status_code == 200:
            print(f"Request {request_id} foi atualizada com o admin_id {admin_id}.")
        else:
            print(f"Erro ao atualizar request {request_id}: {res.status_code}, {res.text}")
