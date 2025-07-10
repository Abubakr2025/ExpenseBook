from fastapi import HTTPException
from starlette import status

from db.models import Category
from pkg.repositories import category as category_repository
from schemas.categoty import AddCategory, UpdateCategory


def check_users_role(user_role):
    if user_role == "user":
        return True
    return False


def get_all_categories(user_id):
    cotegories = category_repository.get_all_categories(user_id)
    if cotegories is None:
        return None
    return cotegories


def get_category_by_id(category_id, user_id):
    get_users_category = category_repository.is_category_user(category_id, user_id)
    if get_users_category is False:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource"
        )
    cotegories = category_repository.get_category_by_id(category_id)
    if cotegories is None:
        return None
    return cotegories


def get_category_by_name(category_name):
    category_from_db = category_repository.get_category_by_name(category_name)
    if category_from_db:
        return category_from_db
    return None


def create_category(category: AddCategory, user_id):
    allowed_types_of_transaction = {"income", "expense"}
    if category.transaction_type not in allowed_types_of_transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Transaction type is invalid. Choose "income" or "expense".'
        )

    c = Category()
    c.name = category.name
    c.transaction_type = category.transaction_type
    c.user_id = user_id
    return category_repository.create_category(c)


def update_category(category_id: int, category: UpdateCategory):
    allowed_types_of_transaction = {"income", "expense"}
    if category.transaction_type not in allowed_types_of_transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Transaction type is invalid. Choose "income" or "expense".'
        )
    return category_repository.update_category(category_id, category)


def soft_delete_category(category_id: int):
    return category_repository.soft_delete_category(category_id)


def hard_delete_category(category_id: int):
    return category_repository.hard_delete(category_id)