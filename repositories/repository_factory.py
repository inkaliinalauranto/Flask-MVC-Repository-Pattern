import os
from repositories.products_repository_mysql import ProductsRepositoryMySQL
from repositories.products_repository_postgres import ProductsRepositoryPostgres
from repositories.users_repository_mysql import UsersRepositoryMySQL
from repositories.users_repository_postgres import UsersRepositoryPostgres


def users_repository_factory():
    _db = os.getenv("DB")

    repo = UsersRepositoryMySQL()

    if _db == "postgres":
        repo = UsersRepositoryPostgres()

    return repo


def products_repository_factory():
    _db = os.getenv("DB")

    repo = ProductsRepositoryMySQL()

    if _db == "postgres":
        repo = ProductsRepositoryPostgres()

    return repo
