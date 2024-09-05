import re

def validate_register(username: str, email: str, password: str, confirm_password: str) -> tuple[bool, str]:
    """
    Valida os campos de registro.

    Args:
        username (str): Nome de usuário.
        email (str): Endereço de email.
        password (str): Senha do usuário.
        confirm_password (str): Confirmação da senha.

    Returns:
        tuple[bool, str]: Retorna um tuple com um booleano indicando se a validação passou
                          e uma mensagem de erro, se houver.
    """
    # Verifica se todos os campos estão preenchidos
    if not username:
        return False, "Ops! Parece que você esqueceu de preencher o nome de usuário."
    if not email:
        return False, "Hmm, o campo de email está vazio. Preenche ele aí!"
    if not password:
        return False, "A senha está faltando! Não se esqueça dela!"
    if not confirm_password:
        return False, "Você precisa confirmar sua senha. Vai que digita errado, né?"

    # Verifica se o nome de usuário é válido
    if not validate_username(username):
        return False, "Opa! O nome de usuário precisa ter pelo menos 3 caracteres e ser alfanumérico."

    # Verifica se o email é válido
    if not validate_email(email):
        return False, "Esse email não parece válido. Dá uma olhada e tenta de novo!"

    # Verifica se a senha é válida
    if not validate_password(password):
        return False, "A senha precisa ter pelo menos 8 caracteres e incluir letras maiúsculas, minúsculas e números."

    # Verifica se a confirmação da senha corresponde à senha
    if password != confirm_password:
        return False, "As senhas não correspondem. Dá uma revisada e tenta de novo."

    return True, "Tudo certo! Vamos em frente!"


def validate_username(username: str) -> bool:
    if len(username) < 3:
        return False
    if not re.match("^[A-Za-z0-9_]+$", username):
        return False
    return True


def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    return True


def validate_login(username: str, password: str) -> tuple[bool, str]:
    """
    Valida os campos de login.

    Args:
        username (str): Nome de usuário.
        password (str): Senha do usuário.

    Returns:
        tuple[bool, str]: Retorna um tuple com um booleano indicando se a validação passou
                          e uma mensagem de erro, se houver.
    """
    # Verifica se todos os campos estão preenchidos
    if not username:
        return False, "Ops! Esqueceu de preencher o nome de usuário."
    if not password:
        return False, "Cadê a senha? Preencha para continuar."

    # Verifica se o nome de usuário é válido
    if not validate_username(username):
        return False, "O nome de usuário deve ter pelo menos 3 caracteres alfanuméricos."

    return True, "Login validado com sucesso!"
