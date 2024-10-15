import os
from repositories.products_repository_mysql import ProductsRepositoryMySQL
from repositories.products_repository_postgres import ProductsRepositoryPostgres
from repositories.users_repository_mysql import UsersRepositoryMySQL
from repositories.users_repository_postgres import UsersRepositoryPostgres


# repository factory käyttäjien controller-funktioille:
def users_repository_factory():
    _db = os.getenv("DB")

    # Oletuksena asetetaan repo-muuttujan arvoksi instanssi
    # UsersRepositoryMySQL-luokasta:
    repo = UsersRepositoryMySQL()

    if _db == "postgres":
        # Jos .env-tiedoston DB-muuttujan arvo on postgres, vaihdetaan
        # repo-muuttujan arvoksi instanssi UsersRepositoryPostgres-luokasta:
        repo = UsersRepositoryPostgres()

    return repo


# repository factory tuotteiden controller-funktioille:
def products_repository_factory():
    _db = os.getenv("DB")

    repo = ProductsRepositoryMySQL()

    if _db == "postgres":
        repo = ProductsRepositoryPostgres()

    return repo
