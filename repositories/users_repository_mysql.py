from repositories.users_repository import UsersRepository


class UsersRepositoryMySQL(UsersRepository):
    def __init__(self):
        super(UsersRepositoryMySQL, self).__init__()
