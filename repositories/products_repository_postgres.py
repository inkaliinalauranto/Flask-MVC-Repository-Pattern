import os
import psycopg2
from models import Product
from repositories.products_repository import ProductsRepository


class ProductsRepositoryPostgres(ProductsRepository):
    def __init__(self):
        self.con = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

        super(ProductsRepositoryPostgres, self).__init__(self.con)

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        # Tähän try-except-blokki, koska con-muuttujalla ei ole
        # is_connected-metodia, joten ei voida laittaa
        # and self.con.is_connected()
        if self.con is not None:
            self.con.close()

    def add(self, name, description):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO products (name, description) "
                        "VALUES (%s, %s) RETURNING *;", (name, description))

            self.con.commit()
            product_tuple = cur.fetchone()

            return Product(_id=product_tuple[0],
                           name=product_tuple[1],
                           description=product_tuple[2])
