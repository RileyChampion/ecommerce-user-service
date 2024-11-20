from sqlalchemy import MetaData
from app.db.session import Base, engine

def drop_db():
    meta = MetaData()
    meta.reflect(bind=engine)
    for table in reversed(meta.sorted_tables):
        print(f"Dropping table {table.name}")
        table.drop(engine)
    print("Database teardown complete.")

if __name__ == "__main__":
    drop_db()