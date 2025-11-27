from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "postgresql+psycopg2://postgres:PASSWORD@localhost:5432/databas"



# --- SQLAlchemy setup ---
Base = declarative_base()

# Skapa engine och session factory
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    """Returnerar en ny databas-session."""
    return SessionLocal()


def create_connection():
    """Alias för get_session()."""
    return get_session()


# Test vid direktkörning
if __name__ == "__main__":
    from sqlalchemy import text

    try:
        with get_session() as session:
            result = session.execute(text("SELECT 1"))
            print("Database connection successful!", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)
