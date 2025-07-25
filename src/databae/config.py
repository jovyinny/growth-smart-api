"""Config."""

from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///.database.sqlite")


def get_db_session() -> Session:
    """Get a database session."""
    with Session(engine) as session:
        yield session
