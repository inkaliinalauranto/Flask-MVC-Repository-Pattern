from models import Product


class ProductsRepository:
    def __init__(self, con):
        self.con = con

    def __del__(self):
        # Tähän try-except-blokki, koska con-muuttujalla ei ole
        # is_connected-metodia, joten ei voida laittaa
        # and self.con.is_connected()
        if self.con is not None:
            self.con.close()

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM products;")
            product_tuples_list = cur.fetchall()

            products_list = [Product(_id=product_tuple[0],
                                     name=product_tuple[1],
                                     description=product_tuple[2])
                             for product_tuple in product_tuples_list]

            return products_list

    def get_by_id(self, product_id):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
            product_tuple = cur.fetchone()

            if product_tuple is None:
                return None

            return Product(_id=product_tuple[0],
                           name=product_tuple[1],
                           description=product_tuple[2])

    def update_by_id(self, product_id, name, description):
        user = self.get_by_id(product_id)

        if user is None:
            return None

        with self.con.cursor() as cur:
            cur.execute("UPDATE products SET name = %s, description = %s "
                        "WHERE id = %s;", (name, description, product_id,))

            self.con.commit()

            return Product(_id=product_id,
                           name=name,
                           description=description)

    def update_lastname_by_id(self, product_id, description):
        product = self.get_by_id(product_id)

        if product is None:
            return None

        with self.con.cursor() as cur:
            cur.execute("UPDATE products SET description = %s WHERE id = %s;",
                        (description, product_id,))

            self.con.commit()

            return Product(_id=product_id,
                           name=product.name,
                           description=description)

    def delete_by_id(self, product_id):
        product = self.get_by_id(product_id)

        if product is None:
            return None

        with self.con.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s;", (product_id,))
            self.con.commit()

            return Product(_id=product_id,
                           name=product.name,
                           description=product.description)
