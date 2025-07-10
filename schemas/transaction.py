from decimal import Decimal

from pydantic import BaseModel


class TransactionSchema(BaseModel):
    amount: Decimal
    description: str
    category_id: int
