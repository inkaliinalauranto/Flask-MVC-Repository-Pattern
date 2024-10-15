from repositories.products_repository import ProductsRepository
import mysql.connector
import os
from models import Product


# Luokka perii ProductsRepository-luokan:
class ProductsRepositoryMySQL(ProductsRepository):
    # Rakentajametodi:
    def __init__(self):
        # Avataan MySQL-tietokantayhteys .env-tiedostoon määritellyillä
        # MySQL-tietokannan tiedoilla:
        self.con = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PASSWORD"))

        # Kutsutaan yliluokan rakentajaa, jonka jäsenmuuttujaksi välitetään
        # tämän luokan jäsenmuuttuja eli avattu tietokantayhteys:
        super(ProductsRepositoryMySQL, self).__init__(self.con)

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()

    # Tuotteen tietokantaan lisäävä metodi on RUD-metodeista poiketen
    # määritelty aliluokassa, koska toteutus on erilainen riippuen siitä,
    # onko käyttöön valittu MySQL- vai PostgreSQL-tietokanta. Metodi lisää
    # tuotteen tietokantaan parametreina saaduilla arvoilla. Metodista
    # palautetaan Product-luokan instanssi uuden tuotteen tiedoilla.
    def add(self, name, description):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO products (name, description) "
                        "VALUES (%s, %s);", (name, description))

            self.con.commit()

            return Product(_id=cur.lastrowid,
                           name=name,
                           description=description)
