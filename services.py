import requests
from config import URL, KEY


class Fetch:
    users = []
    admins = []

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
        print(f"Conteúdo da resposta: {res.text}")

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
        print(f"Conteúdo da resposta (admins): {res.text}")

    @staticmethod
    def fetch_admin_by_username(username):
        url = f'{URL}/rest/v1/admins?username=eq.{username}'
        headers = {
            'apikey': KEY,
            'Authorization': f"Bearer {KEY}"
        }
        res = requests.get(url, headers=headers)

        print(f"Status da resposta (admin): {res.status_code}")
        print(f"Conteúdo da resposta (admin): {res.text}")

        if res.status_code == 200 and len(res.json()) > 0:
            return res.json()[0]
        return None


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
        print(res.text)

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
        print(res.text)

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
