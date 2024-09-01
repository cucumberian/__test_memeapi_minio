from io import BytesIO
from typing import Generator

from minio.error import S3Error
import requests
from minio.helpers import ObjectWriteResult
import pytest

from minio_s3.minio_s3 import MinioS3


@pytest.mark.minio
def test_upload_file(
    minio_instance: "MinioS3",
    file_data: tuple[str, BytesIO, int],
    clean_bucket_fixture,
):
    name, bytes_io, length_io = file_data

    result = minio_instance.upload_file(
        name=name, binary_io=bytes_io, length=length_io
    )
    assert result is not None
    assert result.object_name == name
    assert result.bucket_name == minio_instance.bucket_name


@pytest.mark.minio
def test_stat(
    minio_instance: "MinioS3",
    file_data: tuple[str, BytesIO, int],
    clean_bucket_fixture,
):
    name, bytes_io, length_io = file_data
    minio_instance.upload_file(name=name, binary_io=bytes_io, length=length_io)
    stats = minio_instance.stats(name=name)
    assert stats.size == length_io
    assert stats.object_name == name
    assert stats.bucket_name == minio_instance.bucket_name


@pytest.mark.minio
def test_get_url(
    minio_instance: "MinioS3",
    clean_bucket_fixture,
    uploaded_file: tuple[ObjectWriteResult, BytesIO],
):
    object, bytes_io = uploaded_file
    url = minio_instance.get_url(name=object.object_name)
    assert url


@pytest.mark.minio
def test_url_content(
    minio_instance: "MinioS3",
    clean_bucket_fixture,
    uploaded_file: tuple[ObjectWriteResult, BytesIO],
):
    object, bytes_io = uploaded_file
    url = minio_instance.get_url(name=object.object_name)
    response = requests.get(url)
    assert response.ok
    body = response.content
    assert body == bytes_io.getvalue()


@pytest.mark.minio
def test_download_file(
    minio_instance: "MinioS3",
    clean_bucket_fixture,
    uploaded_file: tuple[ObjectWriteResult, BytesIO],
):
    object, bytes_io = uploaded_file
    b_gen: Generator[bytes, Any, None] = minio_instance.download_file(
        name=object.object_name
    )
    result_bytes = b"".join(b_gen)
    assert result_bytes == bytes_io.getvalue()


@pytest.mark.minio
def test_remove_object(
    minio_instance: "MinioS3",
    clean_bucket_fixture,
    uploaded_file: tuple[ObjectWriteResult, BytesIO],
):
    object, _ = uploaded_file
    minio_instance.remove_object(name=object.object_name)
    with pytest.raises(S3Error):
        minio_instance.stats(name=object.object_name)


def test_remove_objects(
    minio_instance: "MinioS3",
    clean_bucket_fixture,
    uploaded_file: tuple[ObjectWriteResult, BytesIO],
):
    object, bytes = uploaded_file
    objects = minio_instance.get_files()
    assert len(objects) == 1
    minio_instance.remove_objects(object_names=[object.object_name])
    objects = minio_instance.get_files()
    assert len(objects) == 0
