import os
import psycopg2
import models


class ProductsRepositoryPostgres:
    def __init__(self):
        self.con = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

    def __del__(self):
        # Tähän esim. try-except-blokki
        if self.con is not None:
            self.con.close()

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM products;")
            result = cur.fetchall()
            # Palauttaa listan tupleja, esim:
            # [(1, 'testituote1', 'Onkohan tämä lisätty tietokantaan')]
            print(result)
            products = [models.Product(product[0], product[1], product[2])
                        for product in result]

            return products
