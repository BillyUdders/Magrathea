from sqlalchemy import create_engine, Column, String, Integer, LargeBinary
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Map(Base):
    __tablename__ = "maps"

    id = Column(String, primary_key=True, index=True)
    size = Column(Integer)
    octaves = Column(Integer)
    data = Column(LargeBinary)

# Default to a local file, can be overridden for tests
DATABASE_URL = "sqlite:///./magrathea.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
