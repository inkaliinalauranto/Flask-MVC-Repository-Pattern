from repositories.users_repository import UsersRepository


class UsersRepositoryPostgres(UsersRepository):
    def __init__(self):
        super(UsersRepositoryPostgres, self).__init__()
