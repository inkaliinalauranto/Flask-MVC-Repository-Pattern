import os

import mysql.connector

from repositories.users_repository import UsersRepository


class UsersRepositoryMySQL(UsersRepository):
    def __init__(self):
        self.con = self.con = mysql.connector.connect(user=os.getenv("MYSQL_USER"),
                                                      database=os.getenv("DB_NAME"),
                                                      password=os.getenv("MYSQL_PASSWORD"))

        super(UsersRepositoryMySQL, self).__init__(self.con)
