import mysql.connector
import os
import models


class ProductsRepositoryMySQL:
    # Rakentajametodi, jossa avataan tietokantayhteys:
    def __init__(self):
        self.con = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PASSWORD"))

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()

    def get_all(self):
        with self.con.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM products;")
            result = cur.fetchall()
            products = [models.Product(_id=product.get("id"),
                                       name=product.get("name"),
                                       description=product.get("description"))
                        for product in result]

            return products
