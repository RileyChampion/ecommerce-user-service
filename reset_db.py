from setup_db import create_db
from teardown_db import drop_db

if __name__ == "__main__":
    drop_db()
    create_db()