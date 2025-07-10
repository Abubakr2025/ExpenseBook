from sqlalchemy import create_engine
from configs.config import settings

engine = create_engine(settings.database_url)

