from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
import pytest



#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/fastapi_test"

#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:5433/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)


#engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

#Base.metadata.create_all(bind=engine)

#Base = declarative_base()

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db 
    finally:
        db.close()

@pytest.fixture
def client(session):
    # Base.metadata.create_all(bind=engine)

    def override_get_db():
        
        try:
            yield session 
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    #Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


#client = TestClient(app)