from db.db import DatabaseManager
from sqlalchemy import text


def test_connection(db_instance: "DatabaseManager"):
    with db_instance.session() as session:
        cursor = session.execute(text("SELECT 1"))
        result = cursor.scalar_one_or_none()
    assert result == 1
