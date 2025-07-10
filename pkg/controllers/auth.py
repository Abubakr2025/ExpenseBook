import json
from fastapi import APIRouter, status
from starlette.responses import Response


from schemas.user import UserSchema, UserSignInSchema

from pkg.services import user as user_service
from utils.auth import create_access_token

router = APIRouter()


@router.post('/sign-up')
def sign_up(user: UserSchema):
    user_from_db = user_service.get_user_by_username(user.username)
    if user_from_db is not None:
        return Response(json.dumps({'error': 'user with this username already exists'}), status.HTTP_400_BAD_REQUEST)

    user_service.create_user(user)
    return Response(
        json.dumps({'message': 'user created successfully'}),
        status.HTTP_201_CREATED)


@router.post('/sign-in')
def sign_in(user: UserSignInSchema):
    user_from_db = user_service.get_user_by_username_and_password(user.username, user.password)
    if user_from_db is None:
        return Response(json.dumps({'error': 'wrong login or password'}), status.HTTP_404_NOT_FOUND)

    # Создаем JWT токен
    access_token = create_access_token(
        data={
            "id": user_from_db.id,
            "role": user_from_db.role,
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
