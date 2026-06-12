import secrets
import string

def generate_string(length: int = 8) -> str:
    """
    Функция для генерации случайной строки.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
