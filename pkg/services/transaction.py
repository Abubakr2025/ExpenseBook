from fastapi import HTTPException
from starlette import status
from db.models import Transaction

from pkg.repositories import transaction as transaction_repository
from schemas.transaction import TransactionSchema


def is_user_of_transaction(user_id, transaction_id):
    if transaction_repository.get_transaction_by_id(transaction_id) is None:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction doesn't exists with id {transaction_id}"
        )
    return transaction_repository.is_user_of_transaction(user_id, transaction_id)


def check_role(user_role):
    if user_role == "user":
        return True
    return False


def get_all_transactions(user_id):
    get_transactions = transaction_repository.get_all_transactions(user_id)
    return get_transactions


def get_transaction_by_id(transaction_id):
    get_transaction = transaction_repository.get_transaction_by_id(transaction_id)
    return get_transaction


def create_transaction(transaction: TransactionSchema, user_id):
    category_id = transaction.category_id

    if not transaction_repository.is_exists_category(category_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category does not exist"
        )

    if not transaction_repository.is_users_category(category_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this"
        )

    t = Transaction()
    t.amount = transaction.amount
    t.description = transaction.description
    t.category_id = category_id
    t.user_id = user_id
    return transaction_repository.create_transaction(t)


def update_transaction(transaction_id, transaction, user_id):
    if not transaction_repository.is_exists_category(transaction.category_id):
        raise HTTPException(
            status_code=404,
            detail="Category does not exist"
        )
    if not transaction_repository.is_users_category(transaction.category_id, user_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to perform this operation on this category"
        )
    return transaction_repository.update_transaction(transaction_id, transaction, user_id)


def soft_delete_transaction(transaction_id):
    return transaction_repository.soft_delete_transaction(transaction_id)


def delete_transaction(transaction_id):
    return transaction_repository.delete_transaction(transaction_id)
