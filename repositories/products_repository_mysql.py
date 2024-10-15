from repositories.products_repository import ProductsRepository
import mysql.connector
import os
from models import Product


class ProductsRepositoryMySQL(ProductsRepository):
    # Rakentajametodi, jossa avataan tietokantayhteys:
    def __init__(self):
        self.con = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PASSWORD"))

        super(ProductsRepositoryMySQL, self).__init__(self.con)
        print("ProductsRepositoryMySQL(ProductsRepository)-rakentaja: tietokantayhteys luotu")

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()
            print("ProductsRepositoryMySQL(ProductsRepository)-tuhoaja: tietokantayhteys suljettu")

    def add(self, name, description):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO products (name, description) "
                        "VALUES (%s, %s);", (name, description))

            self.con.commit()

            return Product(_id=cur.lastrowid,
                           name=name,
                           description=description)
