import pytest


from db.db import DatabaseManager
from repository.meme_repository import MemeRepo
from schema.meme_schema import MemeDbAdd

from config import ConfigTest


@pytest.fixture(scope="session")
def db_instance():
    print(" * Creating database instance * ")
    db = DatabaseManager(dsn_string=ConfigTest.dsn_string)
    yield db
    db.close()
    print(" * Database instance closed * ")


@pytest.fixture(scope="session")
def repo_instance(db_instance: "DatabaseManager"):
    print(" * Creating repository instance * ")
    repo = MemeRepo(session_manager=db_instance)
    yield repo
    print(" * Repository instance closed * ")


@pytest.fixture(scope="function")
def clean_db_table(repo_instance: "MemeRepo"):
    print(" * Cleaning database table * ")
    repo_instance.clear_table()
    yield
    print(" * Database table cleaned * ")


@pytest.fixture(scope="function")
def added_meme(repo_instance: "MemeRepo"):
    meme = MemeDbAdd(
        text="пример текста мема",
        file_name="meme_image.jpg",
        s3_file_object="mwereir-wekrew3243",
    )
    added_meme = repo_instance.add_meme(meme=meme)
    return added_meme
