from pydantic import BaseModel


class AddCategory(BaseModel):
    name: str
    transaction_type: str


class UpdateCategory(BaseModel):
    name: str
    transaction_type: str
