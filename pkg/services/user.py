import datetime

from logger.logger import logger
from utils.hash import hash_password, verify_password
from pkg.repositories import user as user_repository
from schemas.user import UserSchema
from db.models import User


def get_user_by_username(username):
    user = user_repository.get_user_by_username(username)
    return user


def get_user_by_username_and_password(username, password):
    user = user_repository.get_user_by_username(username)  # Получаем пользователя по username

    if user is None:
        return None

    if not verify_password(password, user.password):
        logger.error(f'Invalid password: {password}')
        return None

    return user


def create_user(user: UserSchema):
    u = User()
    u.full_name = user.full_name
    u.username = user.username
    u.email = user.email
    u.birth_date = user.birth_date
    u.password = hash_password(user.password)
    u.created_at = datetime.datetime.now()
    return user_repository.create_user(u)


def get_all_users():
    return user_repository.get_all_users()
