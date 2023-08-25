from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#SQLAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite:///./db.sqlite:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)  