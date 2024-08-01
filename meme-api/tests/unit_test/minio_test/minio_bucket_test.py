from io import BytesIO
import pytest
from minio.error import S3Error

from minio_s3.minio_s3 import MinioS3

from config import ConfigTest


def test_bucket_exists(minio_instance: "MinioS3"):
    """Test for bucket creation"""
    assert minio_instance.is_bucket_exists(bucket_name=ConfigTest.minio_bucket)


def test_bucket_name_invalid(minio_instance: "MinioS3"):
    invalid_bucket_name = "A_2"
    with pytest.raises(S3Error):
        minio_instance.is_bucket_exists(bucket_name=invalid_bucket_name)


def test_bucket_exists_false(minio_instance: "MinioS3"):
    """Test for bucket exists"""
    fake_bucket_name = "non-existing-bucket-name-akrleqei"
    assert not minio_instance.is_bucket_exists(bucket_name=fake_bucket_name)
