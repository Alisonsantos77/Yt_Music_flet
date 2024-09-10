import requests
from config import URL, KEY
from datetime import datetime, timedelta, timezone
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
            if res.status_code == 200:
                Fetch.users = res.json()
                logger.info(f"{len(Fetch.users)} usuários encontrados")
            else:
                logger.error(f"Erro ao buscar usuários: {res.status_code}, {res.text}")
        except Exception as error:
            logger.error(f"Erro ao buscar usuários: {error}")

        Fetch.group_users_by_last_login()

    @staticmethod
    def fetch_user_or_admin_by_username(username):
        logger.info(f"Buscando por admin ou usuário com username: {username}")

        # Busca o admin pelo username
        admin = Fetch.fetch_admin_by_username(username)
        if admin:
            logger.info(f"Admin {username} encontrado.")
            return admin, "admin"

        # Busca o usuário pelo username
        user = Fetch.fetch_user_by_username(username)
        if user:
            logger.info(f"Usuário {username} encontrado.")
            return user, "user"

        # Se nenhum for encontrado, retorna None
        logger.warning(f"{username} não encontrado como admin ou usuário.")
        return None, None

    @staticmethod
    def validate_user_and_admin_credentials(username, email):
        logger.info(f"Validando existência de username e email: {username}, {email}")

        # Verifica se o username existe na tabela de admins primeiro
        admin = Fetch.fetch_admin_by_username(username)
        if admin:
            logger.info("Username já registrado como administrador.")
            return True, "username"

        # Verifica se o username existe na tabela de usuários
        user = Fetch.fetch_user_by_username(username)
        if user:
            logger.info("Username já registrado como usuário.")
            return True, "username"

        # Verifica se o email já está registrado na tabela de admins
        existing_email_admin = next((adm for adm in Fetch.admins if adm['email'] == email), None)
        if existing_email_admin:
            logger.info("Email já registrado como administrador.")
            return True, "email"

        # Verifica se o email já está registrado na tabela de usuários
        existing_email_user = next((usr for usr in Fetch.users if usr['email'] == email), None)
        if existing_email_user:
            logger.info("Email já registrado como usuário.")
            return True, "email"

        # Se não encontrar conflitos, retorna False
        return False, None

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
                logger.info(f"User {username} encontrado")
                return user
            else:
                logger.warning(f"Usuário {username} não encontrado: {res.status_code}, {res.text}")
                return None
        except Exception as error:
            logger.error(f"Erro ao buscar usuário {username}: {error}")
            return None

    @staticmethod
    def fetch_request_id_by_username(username):
        logger.info(f"Buscando request ID para o usuário {username}")
        try:
            url = f'{URL}/rest/v1/registration_requests?username=eq.{username}&select=id'
            headers = {
                'apikey': KEY,
                'Authorization': f"Bearer {KEY}",
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200 and len(res.json()) > 0:
                request_id = res.json()[0]['id']
                logger.info(f"Request ID {request_id} encontrado para o usuário {username}")
                return request_id
            else:
                logger.warning(f"Erro ao buscar request ID para {username}: {res.status_code}, {res.text}")
                return None
        except Exception as error:
            logger.error(f"Erro ao buscar request ID para {username}: {error}")
            return None

    @staticmethod
    def fetch_all_admins():
        logger.info("Buscando todos os admins")
        try:
            url = f'{URL}/rest/v1/admins?select=*'
            headers = {
                'apikey': KEY,
                'Authorization': f"Bearer {KEY}"
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                Fetch.admins = res.json()
                logger.info(f"{len(Fetch.admins)} admins encontrados")
            else:
                logger.warning(f"Erro ao buscar admins: {res.status_code}, {res.text}")
        except Exception as error:
            logger.error(f"Erro ao buscar admins: {error}")

    @staticmethod
    def fetch_all_requests():
        logger.info("Buscando todas as solicitações de registro")
        try:
            url = f'{URL}/rest/v1/registration_requests?select=*'
            headers = {
                'apikey': KEY,
                'Authorization': f"Bearer {KEY}"
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                Fetch.requests = res.json()
                logger.info(f"{len(Fetch.requests)} solicitações encontradas")
            else:
                logger.warning(f"Erro ao buscar solicitações: {res.status_code}, {res.text}")
        except Exception as error:
            logger.error(f"Erro ao buscar solicitações: {error}")

    @staticmethod
    def fetch_user_or_admin_by_email(email):
        logger.info(f"Verificando se o email {email} já existe.")

        # Busca no banco de admins
        admin = next((adm for adm in Fetch.admins if adm['email'] == email), None)
        if admin:
            logger.info(f"Email já em uso por outro usuário/admin.")
            return True

        # Busca no banco de usuários
        user = next((usr for usr in Fetch.users if usr['email'] == email), None)
        if user:
            logger.info(f"Email já em uso por outro usuário/admin.")
            return True

        return False
    @staticmethod
    def fetch_admin_by_username(username):
        logger.info(f"Buscando admin por username: {username}")
        try:
            url = f'{URL}/rest/v1/admins?username=eq.{username}'
            headers = {
                'apikey': KEY,
                'Authorization': f"Bearer {KEY}"
            }
            res = requests.get(url, headers=headers)
            if res.status_code == 200 and len(res.json()) > 0:
                admin = res.json()[0]
                admin['password'] = decrypt(admin['password'], SECRET_KEY)
                logger.info(f"Admin {username} encontrado")
                return admin
            else:
                logger.warning(f"Admin {username} não encontrado: {res.status_code}, {res.text}")
                return None
        except Exception as error:
            logger.error(f"Erro ao buscar admin {username}: {error}")
            return None

    @staticmethod
    def group_users_by_last_login():
        # Agrupa os usuários pelo último login, considerando os últimos 7 dias
        active_threshold = datetime.now(timezone.utc) - timedelta(days=7)  # Define active_threshold com fuso horário
        grouped_users = {}
        for user in Fetch.users:
            if 'last_login' in user and user['last_login']:
                last_login_date = datetime.fromisoformat(user['last_login'])

                # Verifica se o last_login_date tem fuso horário
                if last_login_date.tzinfo is None:
                    last_login_date = last_login_date.replace(tzinfo=timezone.utc)  # Força o fuso horário UTC

                if last_login_date >= active_threshold:  # Verifica se o login foi nos últimos 7 dias
                    month = last_login_date.strftime("%Y-%m")
                    if month not in grouped_users:
                        grouped_users[month] = 0
                    grouped_users[month] += 1
        Fetch.users_by_last_login = grouped_users
        logger.info(f"Usuários agrupados por último login: {grouped_users}")


class Commit:
    @staticmethod
    def commit_user_to_table(data):
        logger.info("Enviando usuário para a tabela")

        url = f'{URL}/rest/v1/User'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }

        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 201:
            logger.info("Usuário criado com sucesso.")
            return True
        else:
            logger.error(f"Erro ao criar usuário: {res.status_code}, {res.text}")
            return False

    @staticmethod
    def update_last_login(user_id, last_login_time):
        logger.info(f"Atualizando last_login para o usuário ID {user_id}")
        url = f'{URL}/rest/v1/User?id=eq.{user_id}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        update_data = {
            'last_login': last_login_time
        }
        res = requests.patch(url, headers=headers, json=update_data)

        if res.status_code in [200, 204]:
            logger.info(f"last_login atualizado com sucesso para o usuário ID {user_id}")
        else:
            logger.error(f"Erro ao atualizar last_login: {res.status_code}, {res.text}")

    @staticmethod
    def remove_request_from_registration(request_id):
        logger.info(f"Removendo solicitação de registro ID {request_id}")
        url = f'{URL}/rest/v1/registration_requests?id=eq.{request_id}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json',
        }
        res = requests.delete(url, headers=headers)
        if res.status_code in [200, 204]:
            logger.info(f"Request {request_id} foi removida com sucesso.")
            return True
        else:
            logger.error(f"Erro ao remover request {request_id}: {res.status_code}, {res.text}")
            return False

    @staticmethod
    def update_request_with_admin(request_id, admin_id):
        logger.info(f"Atualizando solicitação {request_id} com o admin_id {admin_id}")
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

        if res.status_code in [200, 204]:
            logger.info(f"Solicitação {request_id} atualizada com sucesso pelo Admin ID {admin_id}.")
            return True
        else:
            logger.error(f"Erro ao atualizar solicitação {request_id}: {res.status_code}, {res.text}")
            return False

    @staticmethod
    def commit_registration_request(data):
        url = f'{URL}/rest/v1/registration_requests'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }

        try:
            res = requests.post(url, headers=headers, json=data)
            if res.status_code == 201:
                logger.info(f"Solicitação de registro criada com sucesso para {data['username']}")
            else:
                logger.error(f"Erro ao criar solicitação de registro: {res.status_code}, {res.text}")
        except Exception as e:
            logger.error(f"Erro ao registrar solicitação: {str(e)}")

    @staticmethod
    def commit_admin_to_table(data):
        logger.info("Enviando administrador para a tabela admins")
        encrypted_password = encrypt(data['password'], SECRET_KEY)
        data['password'] = encrypted_password

        url = f'{URL}/rest/v1/admins'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}",
            'Content-Type': 'application/json'
        }
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 201:
            logger.info("Administrador criado com sucesso.")
            return True
        else:
            logger.error(f"Erro ao criar administrador: {res.status_code}, {res.text}")
            return False
