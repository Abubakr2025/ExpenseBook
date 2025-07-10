import datetime
from sqlalchemy.orm import Session
from db.postgres import engine
from db.models import Transaction, User, Category


def is_exists_category(category_id: int) -> bool:
    with Session(bind=engine) as db:
        category = db.query(Category).filter_by(id=category_id).first()
        if category is None or category.deleted_at is not None:
            return False
        return True


def is_users_category(category_id: int, user_id: int) -> bool:
    with Session(bind=engine) as db:
        db_category = db.query(Category).filter_by(id=category_id, user_id=user_id).first()
        if db_category:
            return True
        return False


def is_user_of_transaction(user_id: int, transaction_id) -> bool:
    with Session(bind=engine) as db:
        db_transaction = db.query(Transaction).filter_by(id=transaction_id, user_id=user_id).first()
        if db_transaction:
            return True
        return False


def get_all_transactions(user_id):
    with Session(bind=engine) as db:
        get_transactions = db.query(Transaction).filter_by(user_id=user_id, deleted_at=None).all()
        if get_transactions:
            return get_transactions
        return None


def get_transaction_by_id(transaction_id):
    with Session(bind=engine) as db:
        get_transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if get_transaction is None or get_transaction.deleted_at is not None:
            return None
        return get_transaction


def create_transaction(t: Transaction):
    with Session(bind=engine) as db:
        db.add(t)
        db.commit()
        db.refresh(t)
        return t.id


def update_transaction(transaction_id: int, transaction: Transaction, user_id):
    with Session(bind=engine) as db:
        db_transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if db_transaction:
            db_transaction.amount = transaction.amount
            db_transaction.description = transaction.description
            db_transaction.category_id = transaction.category_id
            db_transaction.user_id = user_id
            db.commit()
            db.refresh(db_transaction)
            return db_transaction.id
        return None


def soft_delete_transaction(transaction_id: int):
    with Session(bind=engine) as db:
        db_transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if db_transaction:
            db_transaction.deleted_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            db.refresh(db_transaction)
            return db_transaction.id
        return None


def delete_transaction(transaction_id: int):
    with Session(bind=engine) as db:
        db_transaction = db.query(Transaction).filter_by(id=transaction_id).first()
        if db_transaction:
            db.delete(db_transaction)
            db.commit()
            return db_transaction.id
        return None
