from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean 
from settings import settings 


if settings.DATABASE_URL.startswith("sqlite"):
   ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("sqlite", "sqlite+aiosqlite", 1)
else:
    ASYNC_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, 
    connect_args={"check_same_thread": False} if "sqlite" in ASYNC_DATABASE_URL else {}
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False, index=True)
    password = Column(String(150), nullable=False)
   
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)