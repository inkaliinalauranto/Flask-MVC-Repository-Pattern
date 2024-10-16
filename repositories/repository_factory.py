import os
from repositories.products_repository_mysql import ProductsRepositoryMySQL
from repositories.products_repository_postgres import ProductsRepositoryPostgres
from repositories.users_repository_mysql import UsersRepositoryMySQL
from repositories.users_repository_postgres import UsersRepositoryPostgres


# repository factory käyttäjien controller-funktioille:
def users_repository_factory():
    _db = os.getenv("DB")

    # Jos tietokantaohjelmistoksi on määritelty .env-tiedostossa MySQL,
    # repo-muuttujaan luodaan instanssi MySQL-repositoriosta:
    if _db == "mysql":
        repo = UsersRepositoryMySQL()
    # Jos taas tietokantaohjelmistoksi on määritelty PostgreSQL, luodaan
    # repo-muuttujaan instanssi PostgreSQL-repositoriosta:
    elif _db == "postgres":
        repo = UsersRepositoryPostgres()
    # Ehdoissa oltava myös else-haara, jotta repo-muuttujalle saadaan arvo
    # kaikenlaisissa tilanteissa:
    else:
        repo = UsersRepositoryMySQL()

    return repo


# repository factory tuotteiden controller-funktioille:
def products_repository_factory():
    _db = os.getenv("DB")

    if _db == "mysql":
        repo = ProductsRepositoryMySQL()
    elif _db == "postgres":
        repo = ProductsRepositoryPostgres()
    else:
        repo = ProductsRepositoryMySQL()

    return repo
