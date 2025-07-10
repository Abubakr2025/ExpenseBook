import datetime
from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Category
from schemas.categoty import UpdateCategory


def is_category_user(category_id: int, user_id: int) -> bool:
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(id=category_id, user_id=user_id).first()
        if db_category:
            return True
        return False


def get_all_categories(user_id):
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(user_id=user_id, deleted_at=None).all()
        if db_category:
            return db_category
        return None


def get_category_by_id(category_id):
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(id=category_id, deleted_at=None).first()
        if db_category:
            return db_category
        return None


def get_category_by_name(category_name):
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(name=category_name).first()
        if db_category:
            return db_category
        return None


def create_category(category: Category):
    with Session(bind=engine) as db:
        db.add(category)
        db.commit()
        db.refresh(category)
        return category.id


def update_category(category_id: int, category: UpdateCategory):
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(id=category_id).first()
        if db_category:
            db_category.name = category.name
            db_category.transaction_type = category.transaction_type
            db_category.updated_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            return db_category.id
        return None


def soft_delete_category(category_id: int):
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(id=category_id).first()
        if db_category:
            db_category.deleted_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            return db_category.id
        return None


def hard_delete(category_id: int):
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(id=category_id).first()
        if db_category:
            db.delete(db_category)
            db.commit()
            return db_category.id
        return None
