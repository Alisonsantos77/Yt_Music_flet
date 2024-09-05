import requests
from config import URL, KEY
from datetime import datetime, timedelta
import os
from config import SECRET_KEY
from flet.security import encrypt, decrypt
from loguru import logger


class Fetch:
    users = []
    admins = []
    requests = []
    users_by_last_login = {}

    @staticmethod
    def fetch_all_users():
        logger.info("Buscando todos os usuários")
        try:
            url = f'{URL}/rest/v1/User?select=*'
            headers = {
                'apikey': KEY,
                'Authorization': f"Bearer {KEY}"
            }
            res = requests.get(url, headers=headers)
            Fetch.users = res.json()
            logger.info(f"{len(Fetch.users)} usuários encontrados")
        except Exception as error:
            logger.error(f"Erro ao buscar usuários: {error}")

        Fetch.group_users_by_last_login()

    @staticmethod
    def fetch_user_by_username(username):
        logger.info(f"Buscando usuário por username: {username}")
        try:
            url = f'{URL}/rest/v1/User?username=eq.{username}'
            headers = {
                'apikey': KEY,
                'Authorization': f"Bearer {KEY}"
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200 and len(res.json()) > 0:
                user = res.json()[0]
                logger.info(f"Usuário {username} encontrado")
                return user
            else:
                logger.warning(f"Usuário {username} não encontrado")
                return None
        except Exception as error:
            logger.error(f"Erro ao buscar usuário {username}: {error}")
            return None

    @staticmethod
    def fetch_request_id_by_username(username):
        url = f'{URL}/rest/v1/registration_requests?username=eq.{username}&select=id'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
        }
        res = requests.get(url, headers=headers)

        if res.status_code == 200 and len(res.json()) > 0:
            request_id = res.json()[0]['id']
            return request_id
        else:
            print(f"Erro ao buscar request ID para {username}: {res.status_code}, {res.text}")
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

    @staticmethod
    def fetch_admin_by_username(username):
        url = f'{URL}/rest/v1/admins?username=eq.{username}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}"
        }
        res = requests.get(url, headers=headers)

        if res.status_code == 200 and len(res.json()) > 0:
            admin = res.json()[0]
            admin['password'] = decrypt(admin['password'], SECRET_KEY)  # Descriptografa a senha
            return admin
        return None

    @staticmethod
    def fetch_and_update_user_table():
        # Atualizar a lista de usuários
        Fetch.fetch_all_users()
        print("Tabela de usuários foi atualizada.")

    @staticmethod
    def group_users_by_last_login():
        # Agrupa os usuários pelo último login
        grouped_users = {}
        for user in Fetch.users:
            if 'last_login' in user and user['last_login']:
                month = datetime.fromisoformat(user['last_login']).strftime("%Y-%m")
                if month not in grouped_users:
                    grouped_users[month] = 0
                grouped_users[month] += 1
        Fetch.users_by_last_login = grouped_users  # Atualiza a variável estática com os usuários agrupados
        print(f"Usuários agrupados por último login: {grouped_users}")

    @staticmethod
    def group_users_by_day(users):
        grouped_users = {}
        for user in users:
            day = datetime.fromisoformat(user['created_at']).strftime("%Y-%m-%d")
            if day not in grouped_users:
                grouped_users[day] = 0
            grouped_users[day] += 1
        return grouped_users

    @staticmethod
    def group_users_by_week(users):
        grouped_users = {}
        for user in users:
            week = (datetime.fromisoformat(user['created_at']) - timedelta(days=datetime.fromisoformat(user['created_at']).weekday())).strftime("%Y-%W")
            if week not in grouped_users:
                grouped_users[week] = 0
            grouped_users[week] += 1
        return grouped_users

    @staticmethod
    def group_users_by_month(users):
        grouped_users = {}
        for user in users:
            month = datetime.fromisoformat(user['created_at']).strftime("%Y-%m")
            if month not in grouped_users:
                grouped_users[month] = 0
            grouped_users[month] += 1
        return grouped_users

class Commit:
    @staticmethod
    def commit_user_to_table(data):
        encrypted_password = encrypt(data['password'], SECRET_KEY)  # Criptografa a senha
        data['password'] = encrypted_password

        url = f'{URL}/rest/v1/User'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        res = requests.post(url, headers=headers, json=data)
        print(res.status_code)

    @staticmethod
    def commit_admin_to_table(data):
        # Criptografando a senha antes de enviar ao banco de dados
        encrypted_password = encrypt(data['password'], SECRET_KEY)
        data['password'] = encrypted_password

        url = f'{URL}/rest/v1/admins'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        res = requests.post(url, headers=headers, json=data)
        print(f"Status da resposta (admin cadastro): {res.status_code}")
        if res.status_code != 201:
            raise Exception(f"Erro ao cadastrar admin: {res.text}")
        print("Admin cadastrado com sucesso!")

    @staticmethod
    def commit_registration_request(data):
        encrypted_password = encrypt(data['password'], SECRET_KEY)  # Criptografa a senha
        data['password'] = encrypted_password

        url = f'{URL}/rest/v1/registration_requests'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        res = requests.post(url, headers=headers, json=data)
        print(res.status_code)

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

    @staticmethod
    def remove_request_from_registration(request_id):
        # URL para deletar uma request pelo ID
        url = f'{URL}/rest/v1/registration_requests?id=eq.{request_id}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json',
        }

        res = requests.delete(url, headers=headers)

        if res.status_code == 200:
            print(f"Request {request_id} foi removida da tabela registration_requests.")
        else:
            print(f"Erro ao remover request {request_id}: {res.status_code}, {res.text}")

    @staticmethod
    def update_request_with_admin(request_id, admin_id):
        # URL para atualizar a request com o campo reviewed_by_admin_id
        url = f'{URL}/rest/v1/registration_requests?id=eq.{request_id}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json',
        }

        update_data = {
            'reviewed_by_admin_id': admin_id,
            'status': 'accepted'
        }

        res = requests.patch(url, headers=headers, json=update_data)

        if res.status_code == 200:
            print(f"Request {request_id} foi atualizada com o admin_id {admin_id}.")
        else:
            print(f"Erro ao atualizar request {request_id}: {res.status_code}, {res.text}")
