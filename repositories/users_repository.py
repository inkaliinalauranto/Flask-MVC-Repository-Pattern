from models import User


class UsersRepository:
    # Rakentajametodi, jossa avataan tietokantayhteys:
    def __init__(self, con):
        self.con = con

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

            users_list = [User(_id=user_tuple[0],
                               username=user_tuple[1],
                               firstname=user_tuple[2],
                               lastname=user_tuple[3])
                          for user_tuple in user_tuple_list]

            return users_list

    def get_by_id(self, user_id):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user_tuple = cur.fetchone()

            if user_tuple is None:
                return None

            return User(_id=user_tuple[0],
                        username=user_tuple[1],
                        firstname=user_tuple[2],
                        lastname=user_tuple[3])

    def update_by_id(self, user_id, username, firstname, lastname):
        user = self.get_by_id(user_id)

        if user is None:
            return None

        with self.con.cursor() as cur:
            cur.execute("UPDATE users "
                        "SET username = %s, firstname = %s, lastname = %s "
                        "WHERE id = %s;",
                        (username, firstname, lastname, user_id,))

            self.con.commit()

            return User(_id=user_id,
                        username=username,
                        firstname=firstname,
                        lastname=lastname)

    def update_lastname_by_id(self, user_id, lastname):
        user = self.get_by_id(user_id)

        if user is None:
            return None

        with self.con.cursor() as cur:
            cur.execute("UPDATE users SET lastname = %s WHERE id = %s;",
                        (lastname, user_id,))

            self.con.commit()

            return User(_id=user_id,
                        username=user.username,
                        firstname=user.firstname,
                        lastname=lastname)

    def delete_by_id(self, user_id):
        user = self.get_by_id(user_id)

        if user is None:
            return None

        with self.con.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            self.con.commit()

            return User(_id=user_id,
                        username=user.username,
                        firstname=user.firstname,
                        lastname=user.lastname)
