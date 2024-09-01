from schema.meme_schema import MemeDbAdd
from schema.meme_schema import MemeDb
from schema.meme_schema import MemeDbModify

from repository.meme_repository import MemeRepo


def test_table_exists(repo_instance: MemeRepo):
    memes = repo_instance.get_all_memes()
    assert isinstance(memes, list)


def test_get_all_memes_empty(
    repo_instance: MemeRepo,
    clean_db_table: None,
):
    memes = repo_instance.get_all_memes()
    assert len(memes) == 0


def test_get_meme_by_id_missing(
    repo_instance: MemeRepo,
    clean_db_table: None,
):
    meme = repo_instance.get_meme_by_id(-1)
    assert meme is None


def test_meme_add(repo_instance: MemeRepo, clean_db_table: None):
    meme_text = "смешной текст"
    meme_file_name = "meme.jpg"
    meme_add = MemeDbAdd(
        text=meme_text,
        file_name=meme_file_name,
        s3_file_object=meme_file_name,
    )
    meme_db = repo_instance.add_meme(meme=meme_add)
    memes = repo_instance.get_all_memes()
    assert meme_db is not None
    assert len(memes) > 0
    assert len(memes) == 1
    assert isinstance(memes[0], MemeDb)
    meme_db_2 = repo_instance.get_meme_by_id(meme_id=meme_db.id)
    assert meme_db_2 == meme_db
    assert memes[0] == meme_db
    assert meme_db.text == meme_text
    assert meme_db.file_name == meme_file_name
    assert meme_db.s3_file_object == meme_file_name


def test_get_meme_by_id(repo_instance: "MemeRepo", added_meme: MemeDb | None):
    if added_meme is None:
        raise AssertionError("Meme not added in added_meme fixture")
    meme_db = repo_instance.get_meme_by_id(meme_id=added_meme.id)
    assert meme_db == added_meme


def test_get_all_memes(
    repo_instance: "MemeRepo",
    added_meme: MemeDb | None,
):
    if added_meme is None:
        raise AssertionError("Meme not added in added_meme fixture")
    memes = repo_instance.get_all_memes()
    assert len(memes) > 0
    assert added_meme in memes


def test_delete_meme_missing(
    repo_instance: "MemeRepo",
    clean_db_table: None,
):
    meme_db = repo_instance.delete_meme(meme_id=-1)
    assert meme_db is None


def test_delete_meme(
    repo_instance: "MemeRepo",
    clean_db_table: None,
    added_meme: MemeDb | None,
):
    assert added_meme is not None

    meme = repo_instance.get_meme_by_id(meme_id=added_meme.id)
    assert meme is not None

    meme_db = repo_instance.delete_meme(meme_id=added_meme.id)
    assert meme_db == added_meme

    none_meme = repo_instance.get_meme_by_id(meme_id=added_meme.id)
    assert none_meme is None


def test_modify_meme(
    repo_instance: "MemeRepo",
    added_meme: MemeDb | None,
):
    assert added_meme is not None

    new_text = added_meme.text + " new text"
    new_file_name = added_meme.file_name + " new_file_name"

    meme_modify = MemeDbModify(
        id=added_meme.id,
        text=new_text,
        file_name=new_file_name,
        s3_file_object=None,
    )

    repo_instance.modify_meme(meme=meme_modify)

    modified_meme = repo_instance.get_meme_by_id(meme_id=added_meme.id)
    assert modified_meme is not None
    assert modified_meme.text == new_text
    assert modified_meme.file_name == new_file_name
    assert modified_meme.s3_file_object == added_meme.s3_file_object
