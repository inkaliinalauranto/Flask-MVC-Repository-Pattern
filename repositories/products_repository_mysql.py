import mysql.connector
import os
from models import Product


class ProductsRepositoryMySQL:
    # Rakentajametodi, jossa avataan tietokantayhteys:
    def __init__(self):
        self.con = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PASSWORD"))

        super(ProductsRepositoryMySQL, self).__init__(self.con)

    def add(self, name, description):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO products (name, description) "
                        "VALUES (%s, %s);", (name, description))

            self.con.commit()

            return Product(_id=cur.lastrowid,
                           name=name,
                           description=description)
