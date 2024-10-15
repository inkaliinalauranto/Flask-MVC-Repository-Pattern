from models import Product


# ProductsRepositoryMySQL- ja ProductsRepositoryPostgres-luokkien yliluokka:
class ProductsRepository:
    # Rakentaja, joka saa (aliluokiltaan) parametrina con-jäsenmuuttujansa
    # arvon. Välitetty arvo on avattu tietokantayhteys.
    def __init__(self, con):
        self.con = con

    '''Jäsenmetodit on toteutettu yliluokkaan, koska ne toimivat sekä 
    MySQL- että PostgreSQL-tietokannoilla'''

    # Metodi, joka hakee tietokannasta kaikki tuotteet. Tuotteet palautetaan
    # listan alkioina, jotka on muutettu Product-luokan instansseiksi:
    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM products;")
            product_tuples_list = cur.fetchall()

            products_list = [Product(_id=product_tuple[0],
                                     name=product_tuple[1],
                                     description=product_tuple[2])
                             for product_tuple in product_tuples_list]

            return products_list

    # Metodi, joka hakee tietokannasta tuotteen id:n perusteella. Jos tuotetta
    # ei haetulla id:llä löydy, palautetaan arvo None. Muussa tapauksessa
    # tuote palautetaan Product-luokan instanssina:
    def get_by_id(self, product_id):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
            product_tuple = cur.fetchone()

            if product_tuple is None:
                return None

            return Product(_id=product_tuple[0],
                           name=product_tuple[1],
                           description=product_tuple[2])

    # Metodi, joka päivittää tuotteen tiedot tietokantaan id:n perusteella:
    def update_by_id(self, product_id, name, description):
        # Tarkistetaan ensin, löytyykö tuotetta välitetyllä id:llä:
        product = self.get_by_id(product_id)

        # Jos tuotetta ei löydy, palataan metodista None-arvolla:
        if product is None:
            return None

        # Muussa tapauksessa päivitetään tuotteen tiedot parametreina
        # saaduilla arvoilla ja palautetaan metodista Product-luokan instanssi
        # päivitetyillä tiedoilla:
        with self.con.cursor() as cur:
            cur.execute("UPDATE products SET name = %s, description = %s "
                        "WHERE id = %s;", (name, description, product_id,))

            self.con.commit()

            return Product(_id=product_id,
                           name=name,
                           description=description)

    # Metodi, joka päivittää tuotteen kuvauksen tietokantaan id:n perusteella:
    def update_description_by_id(self, product_id, description):
        product = self.get_by_id(product_id)

        if product is None:
            return None

        # Jos tuote on olemassa välitetyllä id:llä, päivitetään tuotteen
        # kuvaus parametrina saadulla arvolla ja palautetaan metodista
        # Product-luokan instanssi päivitetyllä kuvauksella:
        with self.con.cursor() as cur:
            cur.execute("UPDATE products SET description = %s WHERE id = %s;",
                        (description, product_id,))

            self.con.commit()

            return Product(_id=product_id,
                           name=product.name,
                           description=description)

    # Metodi, joka poistaa tuotteen tietokannasta id:n perusteella:
    def delete_by_id(self, product_id):
        product = self.get_by_id(product_id)

        if product is None:
            return None

        # Jos tuote on olemassa välitetyllä id:llä, poistetaan tuote ja
        # palautetaan metodista Product-luokan instanssi poistetun tuotteen
        # tiedoilla:
        with self.con.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s;", (product_id,))
            self.con.commit()

            return Product(_id=product_id,
                           name=product.name,
                           description=product.description)
