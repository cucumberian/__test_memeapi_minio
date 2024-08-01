from datetime import timedelta
from typing import BinaryIO
from typing import Iterator

from minio import Minio
from minio.datatypes import Object
from minio.deleteobjects import DeleteObject
from minio.helpers import ObjectWriteResult


class MinioS3:
    def __init__(
        self,
        bucket_name: str,
        access_key: str,
        secret_key: str,
        host: str,
        secure: bool,
    ):
        self.bucket_name = bucket_name
        self.client = Minio(
            endpoint=host,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        self.create_bucket(bucket_name=bucket_name)

    def is_bucket_exists(self, bucket_name: str) -> bool:
        return self.client.bucket_exists(bucket_name=bucket_name)

    def create_bucket(self, bucket_name: str):
        is_bucket = self.client.bucket_exists(bucket_name=bucket_name)
        if not is_bucket:
            self.client.make_bucket(bucket_name=bucket_name)

    def upload_file(
        self, name: str, binary_io: BinaryIO, length: int
    ) -> ObjectWriteResult:
        result = self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=name,
            data=binary_io,
            length=length,
        )
        return result

    def get_files(self) -> list[Object]:
        objects: Iterator[Object] = self.client.list_objects(
            bucket_name=self.bucket_name
        )
        return list(objects)

    def stats(self, name: str) -> Object:
        result = self.client.stat_object(
            bucket_name=self.bucket_name, object_name=name
        )
        return result

    def clear_bucket(self, bucket_name: str | None = None):
        """
        ## Удаление объектов из бакета

        ### Args:
            - `bucket_name (str | None)`: имя бакета. Defaults to None.

        ### Raises:
            - `Exception`: если произошла ошибка при удалении объектов
        """
        if bucket_name is None:
            bucket_name = self.bucket_name
        bucket_objects = self.get_files()
        deleted_objects = (DeleteObject(o.object_name) for o in bucket_objects)
        for error in self.client.remove_objects(
            bucket_name=bucket_name, delete_object_list=deleted_objects
        ):
            raise Exception("Не удалось удалить объект" + str(error))

    def delete_bucket(self, bucket_name: str | None = None):
        """
        ## Удаляет бакет

        ### Args:
            - `bucket_name (str | None, optional)`: Имя бакетя для удаления.
            Если имени нет, то удаляется встроенный бакет, ск оторым работает инстанс.
        """
        if bucket_name is None:
            bucket_name = self.bucket_name

        self.clear_bucket(bucket_name=bucket_name)
        self.client.remove_bucket(bucket_name=bucket_name)

    def get_url(
        self,
        name: str,
        expires: timedelta = timedelta(hours=1),
    ) -> str:
        """
        ## Получение ссылки для скачивания для файла

        ### Args:
            - `name (str)`: имя файла
            - `expires (timedelta, optional)`: время жизни ссылки. [1s, 7d].Defaults is 1 hour.

        ### Returns:
            - `str`: ссылка для скачивания файла
        """

        url = self.client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=name,
            expires=expires,
        )
        return url

    def download_file(self, name: str):
        info = self.client.stat_object(
            bucket_name=self.bucket_name, object_name=name
        )
        total_size = info.size
        if total_size is None:
            raise Exception("File not found")

        offset = 0
        while True:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=name,
                offset=offset,
                length=2048,
            )
            yield response.read()
            offset += 2048
            if offset >= total_size:
                break
