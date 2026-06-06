from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./academyops.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    source = Column(String, nullable=False)
    stage = Column(String, nullable=False)
    notes = Column(Text, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()