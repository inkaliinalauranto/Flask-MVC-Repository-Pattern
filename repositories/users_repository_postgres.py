import os
import psycopg2
from repositories.users_repository import UsersRepository


class UsersRepositoryPostgres(UsersRepository):
    def __init__(self):
        self.con = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

        super(UsersRepositoryPostgres, self).__init__(self.con)
