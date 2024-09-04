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
        return False, "O campo de nome de usuário está vazio."
    if not email:
        return False, "O campo de email está vazio."
    if not password:
        return False, "O campo de senha está vazio."
    if not confirm_password:
        return False, "O campo de confirmação de senha está vazio."

    # Verifica se o nome de usuário é válido
    if not validate_username(username):
        return False, "O nome de usuário é inválido. Use pelo menos 3 caracteres alfanuméricos."

    # Verifica se o email é válido
    if not validate_email(email):
        return False, "O email fornecido é inválido."

    # Verifica se a senha é válida
    if not validate_password(password):
        return False, "A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas e números."

    # Verifica se a confirmação da senha corresponde à senha
    if password != confirm_password:
        return False, "As senhas não correspondem."

    return True, ""


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
        return False, "O campo de nome de usuário está vazio."
    if not password:
        return False, "O campo de senha está vazio."

    # Verifica se o nome de usuário é válido
    if not validate_username(username):
        return False, "O nome de usuário é inválido. Use pelo menos 3 caracteres alfanuméricos."

    return True, ""
