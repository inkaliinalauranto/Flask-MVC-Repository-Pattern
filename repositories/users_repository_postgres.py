import os
import psycopg2
import models


class UsersRepositoryPostgres:
    # Rakentajametodi, jossa avataan tietokantayhteys jäsenmuuttujaan:
    def __init__(self):
        self.con = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

    # Tuhoajametodi, jossa jäsenmuuttujassa oleva tietokantayhteys suljetaan:
    def __del__(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            result = cur.fetchall()
            print(result)
            users = []

            for user in result:
                users.append(models.User(user[0], user[1], user[2], user[3]))

            return users
