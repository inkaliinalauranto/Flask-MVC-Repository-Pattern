import models

class UsersRepository:
    # Rakentajametodi, jossa avataan tietokantayhteys:
    def __init__(self, con):
        self.con = con
        print("Yliluokan rakentajaa kutsuttu - tietokantayhteys avattu")

    # Tuhoajametodi, jossa suljetaan tietokantayhteys:
    def __del__(self):
        # Tähän try-except-blokki, koska con-muuttujalla ei ole
        # is_connected-metodia, joten ei voida laittaa
        # and self.con.is_connected()
        if self.con is not None:
            self.con.close()

        print("Yliluokan rakentaja tuhottu - tietokantayhteys suljettu")

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

    def get_by_id(self, user_id):
        with self.con.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user_tuple = cur.fetchone()
            users = models.User(_id=user_tuple[0],
                                username=user_tuple[1],
                                firstname=user_tuple[2],
                                lastname=user_tuple[3])

            return users
