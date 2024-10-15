import os
import psycopg2
from models import Product
from repositories.products_repository import ProductsRepository


# Luokka perii ProductsRepository-luokan:
class ProductsRepositoryPostgres(ProductsRepository):
    def __init__(self):
        # Avataan PostgreSQL-tietokantayhteys .env-tiedostoon määritellyillä
        # PostgreSQL-tietokannan tiedoilla:
        self.con = psycopg2.connect(f"dbname={os.getenv('DB_NAME')} "
                                    f"user={os.getenv('POSTGRES_USER')} "
                                    f"host={os.getenv('POSTGRES_HOST')} "
                                    f"password={os.getenv('POSTGRES_PW')}")

        # Kutsutaan yliluokan rakentajaa, jonka jäsenmuuttujaksi välitetään
        # tämän luokan jäsenmuuttuja eli avattu tietokantayhteys:
        super(ProductsRepositoryPostgres, self).__init__(self.con)

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        if self.con is not None and not self.con.closed:
            self.con.close()

    # Tuotteen tietokantaan lisäävä metodi on RUD-metodeista poiketen
    # määritelty aliluokassa, koska toteutus on erilainen riippuen siitä,
    # onko käyttöön valittu MySQL- vai PostgreSQL-tietokanta. Metodi lisää
    # tuotteen tietokantaan parametreina saaduilla arvoilla. Metodista
    # palautetaan Product-luokan instanssi uuden tuotteen tiedoilla.
    def add(self, name, description):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO products (name, description) "
                        "VALUES (%s, %s) RETURNING *;", (name, description))

            self.con.commit()
            product_tuple = cur.fetchone()

            return Product(_id=product_tuple[0],
                           name=product_tuple[1],
                           description=product_tuple[2])
