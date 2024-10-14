import os
import psycopg2


class ProductsRepositoryPostgres:
    def __init__(self):
        self.con = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

    def __del__(self):
        if self.con is not None and self.con.is_connected:
            self.con.close()

