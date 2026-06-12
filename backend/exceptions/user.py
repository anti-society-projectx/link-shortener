class UserError(Exception):
    """Базовое исключение для всех ошибок, связанных с пользователями."""
    message: str = "Произошла ошибка при обработке данных пользователя"

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)


class UserNotFoundError(UserError):
    def __init__(self, user_id: int | None = None, tg_id: int | None = None):
        if user_id:
            self.message = f"Пользователь с ID {user_id} не найден"
        elif tg_id:
            self.message = f"Пользователь с tg_id {tg_id} не найден"
        else:
            self.message = "Пользователь не найден"
        super().__init__(self.message)


class UserAlreadyExistsError(UserError):
    """Вызывается при попытке зарегистрировать уже существующий username/tg_id."""
    def __init__(self, tg_id: int):
        self.message = f"Пользователь с tg_id {tg_id} уже зарегистрирован"
        super().__init__(self.message)
