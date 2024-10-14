import os
import mysql.connector
import models


class UsersRepositoryMySQL:
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
            cur.execute("SELECT * FROM users;")
            user_dict_list = cur.fetchall()
            users = [models.User(_id=user_dict.get("id"),
                                 username=user_dict.get("username"),
                                 firstname=user_dict.get("firstname"),
                                 lastname=user_dict.get("lastname"))
                     for user_dict in user_dict_list]

            return users
