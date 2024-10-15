import os
import psycopg2
import models
from repositories.users_repository import UsersRepository


class UsersRepositoryPostgres(UsersRepository):
    def __init__(self):
        self.con = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

        super(UsersRepositoryPostgres, self).__init__(self.con)

    def add(self, username, firstname, lastname):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO users (username, firstname, lastname) "
                        "VALUES (%s, %s, %s) RETURNING *;",
                        (username, firstname, lastname))
            self.con.commit()
            result = cur.fetchone()
            print(result)
            return models.User(_id=result[0],
                               username=result[1],
                               firstname=result[2],
                               lastname=result[3])

