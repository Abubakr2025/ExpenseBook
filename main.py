import uvicorn
from fastapi import FastAPI

from configs.config import settings
from db.models import migrate_tables
from pkg.controllers.auth import router as auth_router
from pkg.controllers.category import router as category_router
from pkg.controllers.transaction import router as transaction_router


if __name__ == '__main__':
    migrate_tables()

    app = FastAPI()
    app.include_router(auth_router)
    app.include_router(category_router)
    app.include_router(transaction_router)
    uvicorn.run(app, port=settings.port, host=settings.host)
