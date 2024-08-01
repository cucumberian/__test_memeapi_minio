import os


class Config:
    minio_access_key = os.environ["MINIO_ACCESS_KEY"]
    minio_secret_key = os.environ["MINIO_SECRET_KEY"]
    minio_host = os.environ["MINIO_HOST"]
    minio_bucket = os.environ["MINIO_BUCKET"]

    postgres_user = os.environ["POSTGRES_USER"]
    postgres_password = os.environ["POSTGRES_PASSWORD"]
    postgres_host = os.environ["POSTGRES_HOST"]
    postgres_port = os.environ["POSTGRES_PORT"]
    postgres_db = os.environ["POSTGRES_DB"]

    sync_dsn = (
        "postgresql+psycopg2://"
        + postgres_user
        + ":"
        + postgres_password
        + "@"
        + postgres_host
        + ":"
        + postgres_port
        + "/"
        + postgres_db
    )


class ConfigTest:
    minio_access_key = os.environ["MINIO_ACCESS_KEY"]
    minio_secret_key = os.environ["MINIO_SECRET_KEY"]
    minio_host = os.environ["MINIO_HOST"]
    minio_bucket = "test-bucket"

    postgres_user = os.environ["POSTGRES_USER"]
    postgres_password = os.environ["POSTGRES_PASSWORD"]
    postgres_host = os.environ["POSTGRES_HOST"]
    postgres_port = os.environ["POSTGRES_PORT"]
    postgres_db = os.environ["POSTGRES_DB"]

    dsn_string = (
        "postgresql+psycopg2://"
        + postgres_user
        + ":"
        + postgres_password
        + "@"
        + postgres_host
        + ":"
        + postgres_port
        + "/"
        + postgres_db
    )
