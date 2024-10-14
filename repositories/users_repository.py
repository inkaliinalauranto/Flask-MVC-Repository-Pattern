import mysql.connector
import os
import models


class UsersRepository:
    # Rakentajametodi, jossa avataan tietokantayhteys:
    def __init__(self):
        self.con = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PASSWORD"))

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        # Tähän try-except-blokki, koska con-muuttujalla ei ole
        # is_connected-metodia, joten ei voida laittaa
        # and self.con.is_connected()
        if self.con is not None:
            self.con.close()

    def get_all(self):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            user_tuple_list = cur.fetchall()
            users = [models.User(_id=user_tuple[0],
                                 username=user_tuple[1],
                                 firstname=user_tuple[2],
                                 lastname=user_tuple[3])
                     for user_tuple in user_tuple_list]

            return users
