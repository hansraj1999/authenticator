from sqlalchemy import create_engine, text
import os

os.system("pip install pymysql")
# Use the same DATABASE_URL as your setup

DATABASE_URL = os.getenv("MYSQL_CONNECTION_STRING")
prefix, rest = DATABASE_URL.split("://", 1)

new_prefix = "mysql+pymysql"
DATABASE_URL = f"{new_prefix}://{rest}"

engine = create_engine(DATABASE_URL)


def drop_tables():
    with engine.connect() as conn:
        # For MySQL, disable foreign key checks before truncation
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))

        # Truncate tables in order (child tables first if needed)
        conn.execute(text("drop TABLE sessions;"))

        conn.execute(text("drop TABLE password_reset_tokens;"))
        conn.execute(text("drop TABLE users;"))

        # Re-enable foreign key checks
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1;"))

        print("Tables truncated successfully.")


# if __name__ == "__main__":
#     truncate_tables()
