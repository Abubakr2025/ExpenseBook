from fastapi import HTTPException, Header, status
from utils.auth import verify_token


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):  # Проверяем, что токен передан корректно
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")

    token = authorization[len("Bearer "):]  # Аккуратно извлекаем сам токен
    payload = verify_token(token)  # Функция валидации токена
    return payload  # Возвращаем расшифрованные данные
