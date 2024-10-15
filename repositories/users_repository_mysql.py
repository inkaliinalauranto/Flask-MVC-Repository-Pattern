import os
import mysql.connector
from models import User
from repositories.users_repository import UsersRepository


class UsersRepositoryMySQL(UsersRepository):
    def __init__(self):
        self.con = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                           database=os.getenv("DB_NAME"),
                                           password=os.getenv("MYSQL_PASSWORD"))

        super(UsersRepositoryMySQL, self).__init__(self.con)

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        if self.con is not None and self.con.is_connected():
            self.con.close()

    def add(self, username, firstname, lastname):
        with self.con.cursor() as cur:
            cur.execute("INSERT INTO users (username, firstname, lastname) "
                        "VALUES (%s, %s, %s);", (username, firstname, lastname))

            self.con.commit()

            return User(_id=cur.lastrowid,
                        username=username,
                        firstname=firstname,
                        lastname=lastname)
