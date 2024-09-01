import pytest

from minio_s3.minio_s3 import MinioS3
from io import BytesIO


@pytest.fixture
def file_data() -> tuple[str, BytesIO, int]:
    """
    Фикстура для создания потока байтов,
    который нужен для тестирования загрузки файла в хранилище

    ### Returns
    - name: str - имя файла
    - bytes_io: BytesIO - поток байтов
    - length: int - длина потока байтов
    """
    name: str = "test.txt"
    string = "test content"
    bytes_io = BytesIO(initial_bytes=string.encode())
    length: int = len(bytes_io.getvalue())
    return name, bytes_io, length


@pytest.fixture
def clean_bucket_fixture(minio_instance: "MinioS3"):
    """
    Фикстура для очистки бакета перед и после теста
    """
    minio_instance.clear_bucket()
    yield
    minio_instance.clear_bucket()


@pytest.fixture
def uploaded_file(
    minio_instance: "MinioS3", file_data: tuple[str, BytesIO, int]
):
    """
    Фикстура для загрузки файла в хранилище
    """
    name, bytes_io, length = file_data
    object = minio_instance.upload_file(
        name=name, binary_io=bytes_io, length=length
    )

    yield object, bytes_io
