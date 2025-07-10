import json
from fastapi import APIRouter, status, Depends, HTTPException
from starlette.responses import Response

from pkg.controllers.middlewares import get_current_user
from pkg.services import category as category_service
from schemas.categoty import AddCategory, UpdateCategory
from utils.auth import TokenPayload

router = APIRouter()


@router.get("/categories", summary="get all categories", tags=['categories'])
def get_all_categories(payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    is_user = category_service.check_users_role(user_role)
    if is_user is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can get categories."
        )
    user_id = payload.id
    categories = category_service.get_all_categories(user_id)
    if categories is None:
        raise HTTPException(
            status_code=404,
            detail="No categories found!"
        )
    return categories


@router.get("/categories/{category_id}", summary="get category by id", tags=['categories'])
def get_category(category_id: int, payload: TokenPayload = Depends(get_current_user)):
    users_id = payload.id
    category = category_service.get_category_by_id(category_id, users_id)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"No category found with id {category_id}!"
        )
    return category


@router.post("/categories", summary="create category", tags=['categories'])
def add_category(category_data: AddCategory, payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    is_user = category_service.check_users_role(user_role)
    if is_user is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can create categories."
        )

    category_exists = category_service.get_category_by_name(category_data.name)
    if category_exists:
        raise HTTPException(
            status_code=407,
            detail="Category already exists."
        )
    user_id = payload.id
    create_category = category_service.create_category(category_data, user_id)
    if create_category:
        return Response(
            json.dumps({'message': f"Category with id {create_category} was created successfully"}),
            status_code=201
        )
    raise HTTPException(
        status_code=400,
        detail="Something went wrong. Please try again."
    )


@router.put('/category/{category_id}', summary="Edit category", tags=['categories'])
def update_category(category_id: int, category_data: UpdateCategory, payload: TokenPayload = Depends(get_current_user)):
    user_role = payload.role
    is_user = category_service.check_users_role(user_role)
    if is_user is False:
        raise HTTPException(
            status_code=403,
            detail="Only users can update categories."
        )
    user_id = payload.id
    category_exists = category_service.get_category_by_id(category_id, user_id)
    if category_exists is None:
        raise HTTPException(
            status_code=404,
            detail=f"No category find with id {category_id}!"
        )
    new_category = category_service.update_category(category_id, category_data)
    if new_category:
        return Response(
            json.dumps({'message': f"Category with id {new_category} was updated successfully!"}),
            status.HTTP_201_CREATED)
    raise HTTPException(
        status_code=400,
        detail="Something went wrong while updating!"
    )


@router.patch('/category/{category_id}', summary="soft delete category", tags=['categories'])
def delete_category(category_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    category_exists = category_service.get_category_by_id(category_id, user_id)
    if category_exists is None:
        raise HTTPException(
            status_code=404,
            detail=f"No category with id {category_id} found!"
        )
    soft_delete_category = category_service.soft_delete_category(category_id)
    if soft_delete_category:
        return Response(
            json.dumps(
                {'message': f"Category with id {soft_delete_category} was deleted successfully"}),
            status_code=200
        )
    raise HTTPException(
        status_code=400,
        detail="Something went wrong while deleting category!"
    )


@router.delete('/category/{category_id}', summary="hard delete category", tags=['categories'])
def hard_delete_category(category_id: int, payload: TokenPayload = Depends(get_current_user)):
    user_id = payload.id
    category_exists = category_service.get_category_by_id(category_id, user_id)
    if category_exists is None:
        raise HTTPException(
            status_code=404,
            detail=f"No category with id {category_id}!"
        )

    hard_delete = category_service.hard_delete_category(category_id)
    if hard_delete:
        return Response(
            json.dumps(
                {'message': f"Category with id {category_id} was deleted successfully"}),
            status.HTTP_200_OK
        )
    raise HTTPException(
        status_code=400,
        detail="Something went wrong while deleting category!"
    )
