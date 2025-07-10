import json
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response

from pkg.controllers.middlewares import get_current_user
from pkg.services import transaction as transaction_service
from utils.auth import TokenPayload
from schemas.transaction import TransactionSchema

router = APIRouter()


@router.get("/transactions", summary="Get all transactions", tags=["transactions"])
def get_all_transactions(payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    is_user = transaction_service.check_role(user_role)
    if is_user is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can get transactions"
        )
    user_id = payload.id
    get_transactions = transaction_service.get_all_transactions(user_id)
    if get_transactions is None:
        raise HTTPException(
            status_code=404,
            detail="No transactions found"
        )
    return get_transactions


@router.get("/transactions/{transaction_id}", summary="Get transaction by id", tags=["transactions"])
def get_transaction_by_id(transaction_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    check_role = transaction_service.check_role(user_role)
    if check_role is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can get transactions"
        )

    get_transaction = transaction_service.get_transaction_by_id(transaction_id)
    if get_transaction is None:
        raise HTTPException(
            status_code=404,
            detail=f"No transaction found with id {transaction_id}"
        )

    user_id = payload.id
    is_user_of_this_transaction = transaction_service.is_user_of_transaction(user_id, transaction_id)
    if is_user_of_this_transaction is False:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this transaction"
        )

    return get_transaction


@router.post("/transactions", summary="Add transaction", tags=["transactions"])
def create_transaction(transaction: TransactionSchema, payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    check_role = transaction_service.check_role(user_role)
    if check_role is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can add transactions"
        )
    user_id = payload.id
    add = transaction_service.create_transaction(transaction, user_id)
    if add:
        return Response(
            json.dumps({"message": f"Transaction added successfully with id {add}"}),
            status_code=201
        )
    raise HTTPException(
        status_code=400,
        detail="Transaction could not be added!"
    )


@router.put("/transactions/{transaction_id}", summary="update transaction by id", tags=["transactions"])
def update_t(transaction_id: int, transaction: TransactionSchema, payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    check_role = transaction_service.check_role(user_role)
    if check_role is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can update transactions"
        )
    user_id = payload.id
    is_user_of_transaction = transaction_service.is_user_of_transaction(user_id, transaction_id)
    if is_user_of_transaction is False:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to modify this transaction"
        )
    updated = transaction_service.update_transaction(transaction_id, transaction, user_id)
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail=f"No transaction found with id {transaction_id}"
        )
    return Response(
        json.dumps({"message": f"Transaction updated successfully with id {transaction_id}"}),
        status_code=200
    )


@router.patch("/transactions/{transaction_id}", summary="soft delete transaction by id", tags=["transactions"])
def soft_delete_transaction(transaction_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    check_role = transaction_service.check_role(user_role)
    if check_role is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can soft delete transactions"
        )
    user_id = payload.id
    is_user_of_transaction = transaction_service.is_user_of_transaction(user_id, transaction_id)
    if is_user_of_transaction is False:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this transaction"
        )
    delete_transaction = transaction_service.soft_delete_transaction(transaction_id)
    if delete_transaction is None:
        raise HTTPException(
            status_code=404,
            detail=f"No transaction found with id {transaction_id}"
        )
    return Response(
        json.dumps({"message": f"Transaction deleted successfully with id {transaction_id}"}),
        status_code=200
    )


@router.delete("/transactions/{transaction_id}", summary="Hard delete transaction by id", tags=["transactions"])
def hard_delete_transaction(transaction_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    check_role = transaction_service.check_role(user_role)
    if check_role is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can delete transactions"
        )
    user_id = payload.id
    is_user_of_transaction = transaction_service.is_user_of_transaction(user_id, transaction_id)
    if is_user_of_transaction is False:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to view this transaction"
        )
    delete = transaction_service.delete_transaction(transaction_id)
    if delete is None:
        raise HTTPException(
            status_code=404,
            detail=f"No transaction found with id {transaction_id}"
        )
    return Response(
        json.dumps({"message": f"Transaction deleted successfully with id {transaction_id}"}),
        status_code=200
    )
