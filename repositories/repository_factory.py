import os
from repositories.users_repository_mysql import UsersRepositoryMySQL
from repositories.users_repository_postgres import UsersRepositoryPostgres


def users_repository_factory():
    _db = os.getenv("DB")

    repo = UsersRepositoryMySQL()

    if _db == "postgres":
        repo = UsersRepositoryPostgres()

    return repo
