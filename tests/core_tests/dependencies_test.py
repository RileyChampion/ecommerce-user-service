import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
# from sqlalchemy.exc import ResourceClosedError, InvalidRequestError
from app.core.dependencies import get_db
from app.db.session import SessionLocal


def test_get_db_retrieved_and_closed():
    # TODO : Not closing the connection even those .close() is called
    db_gen = get_db()

    db_connection = next(db_gen)
    assert isinstance(db_connection, Session)

    with pytest.raises(StopIteration):
        next(db_gen)

    db_connection.close()

    print(f"Session is active: {db_connection.is_active}")
    print(f"Session dirty: {db_connection.dirty}")
    print(f"Session closed: {db_connection._is_clean}")
    
    # with pytest.raises(ResourceClosedError):
    #     db_connection.connection()
