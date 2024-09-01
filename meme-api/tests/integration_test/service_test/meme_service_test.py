import pytest
from service.meme_service import MemeService


def test_get_all_memes(
    meme_service: "MemeService",
    clean_db_table,
):
    memes = meme_service.get_all_memes()
    assert len(memes) > 0


@pytest.mark.skip(reason="Not implemented")
def test_get_all_memes_empty(
    meme_service: "MemeService",
    clean_db_table,
):
    memes = meme_service.get_all_memes()
    assert len(memes) == 0


def test_get_meme_by_id(
    meme_service: "MemeService",
):
    meme = meme_service.get_meme(meme_id=1)
    assert meme is not None


@pytest.mark.skip(reason="Not implemented")
def test_update_meme(
    meme_service: "MemeService",
):
    assert 1 == 0


@pytest.mark.skip(reason="Not implemented")
def test_delete_meme(
    meme_service: "MemeService",
):
    assert 1 == 0
